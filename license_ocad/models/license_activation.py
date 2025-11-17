import logging
import re

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

REQUESTS_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"}


class LicenseActivation(models.TransientModel):
    _name = "license.activation"
    _description = "License Activation"

    _id = fields.Integer("ID", readonly=True)
    name = fields.Char(readonly=True)
    key = fields.Char(readonly=True)
    content = fields.Char(readonly=True)
    status = fields.Integer(readonly=True)
    license_id = fields.Many2one("license.license")

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Reset license activations list when list is shown."""
        license_id = self.env["license.license"].browse(self._context["license_id"])
        if license_id:
            self.sudo().search([("license_id", "=", license_id.id)]).unlink()
            activations_data, license_data = self._get_activations(license_id)
            self.sudo().create(activations_data)
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

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

    def _disable_activation(self):
        message = ""
        for activation in self:
            url = "https://www.ocad.com/ocadintern/db_increaseCounter/deactivateActivation_2018.php"
            params = {
                "productKey": activation.key,
                "licenseNumber": activation.license_id.name,
                "status": 3,
                "id": activation._id,
            }
            auth = (
                activation.license_id.company_id.ocad_username,
                activation.license_id.company_id.ocad_password,
            )

            _logger.info("Send post request to %s", url, exc_info=True)
            response = requests.post(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)
            message += response.text

            if "FEHLER" in message or "Unauthorized" in message:
                raise UserError(_("Error while disabling activation: %s", message))

        return message

    @api.model
    def _get_activations(self, license_id):
        """Retrieve activations data from license activation server."""

        edition_short = str(license_id.product_id.get_value_by_key("EditionShort"))

        ocad_username = license_id.company_id.ocad_username
        ocad_password = license_id.company_id.ocad_password

        if ocad_username and ocad_password and edition_short and license_id.name != _("New"):
            url = "https://www.ocad.com/ocadintern/db_increaseCounter/getActivations_2018.php"
            params = {
                "edition": edition_short,
                "licenseNumber": license_id.name,
            }
            auth = (
                ocad_username,
                ocad_password,
            )

            _logger.info("Send get request to %s", url, exc_info=True)
            response = requests.get(url, params=params, auth=auth, timeout=10, headers=REQUESTS_HEADERS)

            # Reponse is a semicolon separated string that has to be processed
            columns = 13
            cells = response.text.split(";")
            rows = len(cells) // columns

            activations = []
            for i in range(0, rows):
                start = i * columns
                end = start + columns

                status = re.search(r".+\(\s(.+)\s\)", cells[start])

                activations.append(
                    {
                        "_id": cells[end - 1],
                        "name": cells[start],
                        "key": cells[start + 1],
                        "content": " ".join(cells[start + 2 : end]),
                        "status": status.group(1) if status else 0,
                        "license_id": license_id.id,
                    }
                )

            # License activation data from fourth last cell
            if len(cells) > 3:
                license_data = {
                    "active_activations": cells[-4] or 0,
                    "registered_activations": cells[-3] or 0,
                    "max_activations": cells[-2] or 0,
                }
            else:
                # Not enough data — default to 0
                license_data = {
                    "active_activations": 0,
                    "registered_activations": 0,
                    "max_activations": 0,
                }

            return activations, license_data
        else:
            return False, False

    # Model Actions

    def action_disable(self):
        message = self._disable_activation()
        return self._get_client_notification_action(message)
