import logging
import random
import urllib

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from . import ocad

_logger = logging.getLogger(__name__)


def _get_download_token():
    char_table = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"  # 58 char
    token = ""
    for _ in range(8):
        token += char_table[random.randint(0, 57)]
    return token


REQUESTS_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"}


class License(models.Model):
    _inherit = "license.license"

    # Update Fields

    client_order_ref = fields.Char(required=True)

    # New Fields

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    download_token = fields.Char(readonly=False, tracking=True)
    download_link = fields.Char(compute="_compute_links", readonly=True, store=True)
    update_link = fields.Char(compute="_compute_links", readonly=True, store=True)
    registered = fields.Boolean(readonly=True, help="License registered with Odoo.")
    active_activations = fields.Integer(compute="_compute_license_activations", compute_sudo=True, readonly=True)
    registered_activations = fields.Integer(compute="_compute_license_activations", compute_sudo=True, readonly=True)
    max_activations = fields.Integer(
        compute="_compute_license_activations",
        compute_sudo=True,
        store=True,
        readonly=True,
    )
    runtime = fields.Integer(
        compute="_compute_runtime",
        readonly=True,
        store=True,
        help="Computed from production information attribute.",
    )
    date_end = fields.Date(inverse="_inverse_date_end")

    # Compute fields

    def _inverse_date_end(self):
        for license in self:
            license._update_end_date()

    @api.depends("product_id")
    def _compute_runtime(self):
        for license in self:
            if license.product_id and license.name != _("New"):
                license.runtime = license.product_id.get_value_by_key("Runtime") * 12

    def _compute_license_activations(self):
        for license in self:
            if len(self) == 1:
                activations, license_data = self.env["license.activation"]._get_activations(license)
                if license_data:
                    license.active_activations = license_data["active_activations"]
                    license.registered_activations = license_data["registered_activations"]
                    license.max_activations = license_data["max_activations"]
                else:
                    license.active_activations = 0
                    license.registered_activations = 0
            else:
                license.active_activations = 0
                license.registered_activations = 0

    # Model methods

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val.get("download_token"):
                val["download_token"] = _get_download_token()
        return super().create(vals_list)

    # Helper Methods

    def _get_client_notification_action(self, message):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "OCAD License Service",
                "message": message,
                "sticky": False,
                "type": "success",
                "next": {"type": "ir.actions.act_window_close"},  # Refresh the form
            },
        }

    # API Methods

    @api.depends("name", "product_id", "download_token", "key")
    def _compute_links(self):
        """Generate download and update link."""
        for license in self:
            if license.product_id and license.name != _("New"):
                edition_short = str(license.product_id.get_value_by_key("EditionShort"))
                version = str(license.product_id.get_value_by_key("Version"))

                if edition_short != "None" and version != "None" and license.download_token:
                    license.download_link = (
                        "https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e="
                        + edition_short
                        + "&l="
                        + license.name
                        + "&v="
                        + version
                        + "&d="
                        + license.download_token
                    )
                    license.update_link = (
                        "https://www.ocad.com/OCAD2018/OCAD_2018_Update.php?e="
                        + edition_short
                        + "&l="
                        + license.name
                        + "&v="
                        + version
                        + "&c="
                        + license.key
                    )

    @api.depends("name", "product_id", "partner_id", "client_order_ref")
    def _compute_key(self):
        for license in self:
            if license.product_id and license.client_order_ref and license.name != _("New"):
                version = license.product_id.get_value_by_key("Version")
                edition_long = license.product_id.get_value_by_key("EditionLong")

                if not version or not edition_long:
                    raise UserError(_("Missing product information fields"))

                license.key = "".join(
                    ocad.get_ocad2018_checksum(
                        version,
                        int(license.name),
                        edition_long,
                        license.client_order_ref,
                    )
                )

    def _create_license(self):
        message = ""
        ocad_username = self.company_id.ocad_username
        ocad_password = self.company_id.ocad_password

        if ocad_username and ocad_password:
            for license in self:
                edition_short = license.product_id.get_value_by_key("EditionShort")
                number_of_activations = license.product_id.get_value_by_key("NumberOfActivations")
                is_team = license.product_id.get_value_by_key("IsTeam")
                checksum = "".join(substring[0] for substring in license.key.split("-"))
                license.product_id.get_value_by_key("Version")

                # Create entry in license activation database
                url = "https://www.ocad.com/ocadintern/db_newlicense/UpdateNewLicense2018.php"
                params = {
                    "licenseNumber": license.name,
                    "edition": edition_short,
                    "checkSum": checksum,
                    "dwnlink": license.download_token,
                    "numberOfActivations": number_of_activations,
                    "subBegin": license.date_start.strftime("%Y-%m-%d"),
                    "subEnd": license.date_end.strftime("%Y-%m-%d"),
                    "isTeam": is_team,
                    "reseller": "",
                    "renewal": "true" if license.parent_sale_line_id else "false",
                }
                auth = (ocad_username, ocad_password)

                _logger.info("Send post request to %s", url, exc_info=True)
                license.message_post(body=_("Send request to %s.", url))
                response = requests.post(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)
                message = response.text

                if message != "FEHLER: Lizenznummer schon in Datenbank vorhanden!" and (
                    "FEHLER" in message or "Unauthorized" in message
                ):
                    raise UserError(_("Error while creating license: %s", message))

        return message

    def _update_license(self):
        message = ""
        ocad_username = self.company_id.ocad_username
        ocad_password = self.company_id.ocad_password

        if ocad_username and ocad_password:
            for license in self:
                edition_short = license.product_id.get_value_by_key("EditionShort")
                version = license.product_id.get_value_by_key("Version")

                # Create entry in license manager database
                url = "https://www.ocad.com/ocadintern/db_newlicense/UpdateLicense.php"
                params = {
                    "LicenseNumber": license.name,
                    "EditionShort": edition_short,
                    "Version": version,
                    "LicenseName": urllib.parse.quote(license.client_order_ref),
                }
                auth = (ocad_username, ocad_password)

                _logger.info("Send post request to %s", url, exc_info=True)
                license.message_post(body=_("Send request to %s.", url))
                response = requests.post(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)
                message = response.text

                if "FEHLER" in message or "Unauthorized" in message:
                    raise UserError(_("Error while updating license: %s", message))

        return message

    def _increase_counter(self):
        message = ""
        ocad_username = self.company_id.ocad_username
        ocad_password = self.company_id.ocad_password

        if ocad_username and ocad_password:
            for license in self:
                edition_short = license.product_id.get_value_by_key("EditionShort")

                url = "https://www.ocad.com/ocadintern/db_increaseCounter/increaseCounter_2018.php"
                params = {
                    "licenseNumber": license.name,
                    "edition": edition_short,
                }
                auth = (ocad_username, ocad_password)

                _logger.info("Send post request to %s", url, exc_info=True)
                license.message_post(body=_("Send request to %s.", url))
                response = requests.post(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)
                message = response.text

                if "FEHLER" in message or "Unauthorized" in message:
                    raise UserError(_("Error while increasing counter: %s", message))

        return message

    def _update_end_date(self):
        message = ""
        ocad_username = self.company_id.ocad_username
        ocad_password = self.company_id.ocad_password

        if ocad_username and ocad_password:
            for license in self.filtered(lambda r: r.state == "active" and r.date_end):
                edition_short = license.product_id.get_value_by_key("EditionShort")

                url = "https://www.ocad.com/ocadintern/db_newlicense/UpdateSubscriptionEndDate2018.php"
                params = {
                    "licenseNumber": license.name,
                    "edition": edition_short,
                    "subEnd": license.date_end.strftime("%Y-%m-%d"),
                }
                auth = (ocad_username, ocad_password)

                _logger.info("Send post request to %s", url, exc_info=True)
                license.message_post(body=_("Send request to %s.", url))
                response = requests.post(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)
                message = response.text

                if "FEHLER" in message or "Unauthorized" in message:
                    raise UserError(_("Error while updating end date: %s", message))

        return message

    def _update_license_status(self, valid=True):
        message = ""
        ocad_username = self.company_id.ocad_username
        ocad_password = self.company_id.ocad_password

        if ocad_username and ocad_password:
            for license in self:
                edition_short = license.product_id.get_value_by_key("EditionShort")

                url = "https://www.ocad.com/ocadintern/db_newlicense/UpdateLicenseStatus_2018.php"
                params = {
                    "licenseNumber": license.name,
                    "edition": edition_short,
                    "valid": 1 if valid else 0,
                }
                auth = (ocad_username, ocad_password)

                _logger.info("Send post request to %s", url, exc_info=True)
                license.message_post(body=_("Send request to %s.", url))
                response = requests.post(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)
                message = response.text

                if "FEHLER" in message or "Unauthorized" in message:
                    raise UserError(_("Error while updating license status: %s", message))

        return message

    # Model Actions

    def action_activate(self):
        """Create and enable license."""
        super().action_activate()

        message = self._create_license()  # Create entry in license database
        message += self._update_license()  # Create entry in activation database

        for license in self:
            license.write(
                {
                    "registered": True,
                    "max_activations": license.product_id.get_value_by_key("NumberOfActivations"),
                }
            )

        return self._get_client_notification_action(message)

    def action_update(self):
        """Update license."""
        message = self._update_license()
        return self._get_client_notification_action(message)

    def action_disable(self):
        super().action_disable()
        message = self._update_license_status(valid=False)
        return self._get_client_notification_action(message)

    def action_enable(self):
        super().action_enable()
        message = self._update_license_status(valid=True)
        return self._get_client_notification_action(message)

    def action_unlock(self):
        message = self._increase_counter()

        for license in self:
            self.write({"max_activations": license.max_activations + 1})

        return self._get_client_notification_action(message)

    def action_update_end_date(self):
        message = self._update_end_date()
        return self._get_client_notification_action(message)

    def action_view_activations(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "license.activation",
            "name": _("License Activations"),
            "view_mode": "list",
            "views": [[False, "list"]],
            "context": {"license_id": self.id},
            "domain": [("license_id", "=", self.id)],
        }

    def action_view_status(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "license.status",
            "name": _("License Status"),
            "view_mode": "list",
            "views": [[False, "list"]],
            "context": {"license_id": self.id},
            "domain": [("license_id", "=", self.id)],
        }
