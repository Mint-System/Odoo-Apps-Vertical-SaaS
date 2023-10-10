import logging

import requests

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class LicenseStatus(models.TransientModel):
    _name = "license.status"
    _description = "License Status"

    _id = fields.Integer("ID", readonly=True)
    name = fields.Char(readonly=True)
    license_id = fields.Many2one("license.license")

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Reset license activations list when list is shown."""

        license_id = self.env["license.license"].browse(self._context["license_id"])
        if license_id:
            self.sudo().search([("license_id", "=", license_id.id)]).unlink()
            activation_status_data = self._get_activation_status(license_id)
            self.sudo().create(activation_status_data)

        return super().search_read(
            domain=domain, fields=fields, offset=offset, limit=limit, order=order
        )

    @api.model
    def _get_activation_status(self, license_id):
        """Retrieve activations status data from license activation server."""

        edition_short = str(license_id.product_id.get_value_by_key("EditionShort"))

        if edition_short and license_id.name != _("New"):

            url = "https://www.ocad.com/ocadintern/db_increaseCounter/getActivationStatus_2018.php"
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
            activation_status = []
            for i in range(0, rows):
                start = i * columns
                end = start + columns

                activation_status.append(
                    {"name": " ".join(cells[start:end]), "license_id": license_id.id}
                )

            return activation_status
