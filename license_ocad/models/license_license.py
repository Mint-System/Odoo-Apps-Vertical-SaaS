import logging
import random

import requests

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)
from . import ocad


class License(models.Model):
    _inherit = "license.license"

    # Existing fields
    client_order_ref = fields.Char(required=True)

    # New fields
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    download_token = fields.Char(
        compute="_compute_download_token", readonly=False, store=True, precompute=True
    )
    download_link = fields.Char(
        compute="_compute_download_links", readonly=True, store=True
    )
    update_link = fields.Char(
        compute="_compute_download_links", readonly=True, store=True
    )
    registered = fields.Boolean(readonly=True)
    active_activations = fields.Integer(readonly=True)
    registered_activations = fields.Integer(readonly=True)
    max_activations = fields.Integer(readonly=True)
    runtime = fields.Integer(compute="_compute_runtime", readonly=False, store=True)

    @api.depends("product_id")
    def _compute_runtime(self):
        for license in self:
            if license.product_id and license.name != _("New"):
                license.runtime = license.product_id.get_value_by_key("Runtime") * 12

    @api.depends("name")
    def _compute_download_token(self):
        char_table = (
            "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"  # 58 char
        )
        for license in self:
            result = ""
            for _ in range(8):
                result += char_table[
                    random.randint(0, 57)
                ]  # randint includes both ends of the range
            license.download_token = result

    @api.depends("name", "product_id", "download_token", "key")
    def _compute_download_links(self):
        """Generate download link."""
        for license in self:
            if license.product_id and license.name != _("New"):
                edition_short = str(license.product_id.get_value_by_key("EditionShort"))
                version = str(license.product_id.get_value_by_key("Version"))
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
            if (
                license.product_id
                and license.client_order_ref
                and license.name != _("New")
            ):
                version = license.product_id.get_value_by_key("Version")
                edition_long = license.product_id.get_value_by_key("EditionLong")
                # Values: 2018, 5002, 'Mapping Solution', 'OCAD AG'
                # Result: 5E27-8047-C507
                # Values: 2018, 60019, 'Course Setting', 'OLK Fricktal'
                # Result: 7A8A-4F7F-7086
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
        for license in self:

            edition_short = license.product_id.get_value_by_key("EditionShort")
            number_of_activations = license.product_id.get_value_by_key(
                "NumberOfActivations"
            )
            is_team = license.product_id.get_value_by_key("IsTeam")
            checksum = "".join(substring[0] for substring in license.key.split("-"))

            url = (
                "https://www.ocad.com/ocadintern/db_newlicense/UpdateNewLicense2018.php"
            )
            params = {
                "edition": edition_short,
                "licenseNumber": license.name,
                "checkSum": checksum,
                "dwnlink": license.download_token,
                "numberOfActivations": number_of_activations,
                "subBegin": license.date_start.strftime("%Y-%m-%d"),
                "subEnd": license.date_end.strftime("%Y-%m-%d"),
                "isTeam": is_team,
                "reseller": "",
            }
            auth = (self.company_id.ocad_username, self.company_id.ocad_password)

            response = requests.post(url, params=params, auth=auth)
            message += response.text + "\n"

        return message

    def _increase_counter(self):
        message = ""
        for license in self:

            edition_short = license.product_id.get_value_by_key("EditionShort")

            url = "https://www.ocad.com/ocadintern/db_increaseCounter/increaseCounter_2018.php"
            params = {
                "edition": edition_short,
                "licenseNumber": license.name,
            }
            auth = (self.company_id.ocad_username, self.company_id.ocad_password)

            response = requests.post(url, params=params, auth=auth)
            message += response.text + "\n"

        return message

    def _get_action_notification(self, message):
        notification_type = "success"
        notification_sticky = False
        if "FEHLER" in message or "Unauthorized" in message:
            notification_type = "danger"
            notification_sticky = True

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "OCAD License Service",
                "message": message,
                "sticky": notification_sticky,
                "type": notification_type,
                "next": {"type": "ir.actions.act_window_close"},  # Refresh the form
            },
        }

    def action_activate(self):
        """Create and enable license."""
        super().action_activate()

        message = self._create_license()

        if not ("FEHLER" in message or "Unauthorized" in message):
            for license in self:
                license.write(
                    {
                        "registered": True,
                        "max_activations": license.product_id.get_value_by_key(
                            "NumberOfActivations"
                        ),
                    }
                )

        return self._get_action_notification(message)

    def action_unlock(self):
        message = self._increase_counter()

        if not ("FEHLER" in message or "Unauthorized" in message):
            for license in self:
                self.write({"max_activations": license.max_activations + 1})

        return self._get_action_notification(message)

    def action_get_activations(self):
        self.env["license.activation"].get_activations(self)

    def action_view_activations(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "license.activation",
            "name": _("License Activations"),
            "view_mode": "tree",
            "views": [[False, "list"]],
            "context": {"license_id": self.id},
            "domain": [("license_id", "=", self.id)],
        }

    def action_view_status(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "license.status",
            "name": _("License Status"),
            "view_mode": "tree",
            "views": [[False, "list"]],
            "context": {"license_id": self.id},
            "domain": [("license_id", "=", self.id)],
        }
