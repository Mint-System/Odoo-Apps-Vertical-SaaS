import logging
import re

import requests

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


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
    def get_activations(self, license_id):
        self.sudo().search([("license_id", "=", license_id.id)]).unlink()
        activations_data, license_data = self._get_activations(license_id)
        license_id.write(license_data)
        self.sudo().create(activations_data)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Reset license activations list when list is shown."""
        license_id = self.env["license.license"].browse(self._context["license_id"])
        if license_id:
            self.get_activations(license_id)
        return super().search_read(
            domain=domain, fields=fields, offset=offset, limit=limit, order=order
        )

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

            response = requests.post(url, params=params, auth=auth)
            message += response.text + "\n"

        return message

    @api.model
    def _get_activations(self, license_id):
        """Retrieve activations data from license activation server."""

        edition_short = str(license_id.product_id.get_value_by_key("EditionShort"))

        if edition_short and license_id.name != _("New"):

            url = "https://www.ocad.com/ocadintern/db_increaseCounter/getActivations_2018.php"
            params = {
                "edition": edition_short,
                "licenseNumber": license_id.name,
            }
            auth = (
                license_id.company_id.ocad_username,
                license_id.company_id.ocad_password,
            )

            response = requests.get(url, params=params, auth=auth)

            # Reponse is a semicolon separated string that has to be processed
            columns = 13
            cells = response.text.split(";")
            rows = len(cells) // columns

            activations = []
            for i in range(0, rows):
                start = i * columns
                end = start + columns

                status = re.search(".+\(\s(.+)\s\)", cells[start])

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

            # Last 3 cels contain license activation data
            start = rows * columns
            license_data = {
                "active_activations": cells[start],
                "registered_activations": cells[start + 1],
                "max_activations": cells[start + 2],
            }

            return activations, license_data

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

    def action_disable(self):
        message = self._disable_activation()
        return self._get_action_notification(message)
