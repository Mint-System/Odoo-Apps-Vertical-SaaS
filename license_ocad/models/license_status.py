import logging

import requests

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class LicenseStatus(models.TransientModel):
    _name = "license.status"
    _description = "License Status"

    _id = fields.Integer("ID", readonly=True)
    license_id = fields.Many2one("license.license")
    # 13 fields
    name = fields.Char(readonly=True, string="ID")
    license_number = fields.Char(readonly=True)
    license_status = fields.Char(readonly=True)
    build = fields.Char(readonly=True)
    uuid = fields.Char(readonly=True)
    ip = fields.Char(readonly=True)
    country = fields.Char(readonly=True)
    timestamp = fields.Char(readonly=True)
    performance = fields.Char(readonly=True)
    product_key = fields.Char(readonly=True)
    windows_version = fields.Char(readonly=True)
    computer_name = fields.Char(readonly=True)
    parameter_change = fields.Char(readonly=True)

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

    # === API Methods ===#

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
                start + columns

                activation_status.append(
                    {
                        "license_id": license_id.id,
                        "name": cells[start],
                        "license_number": cells[start + 1],
                        "license_status": cells[start + 2],
                        "build": cells[start + 3],
                        "uuid": cells[start + 4],
                        "ip": cells[start + 5],
                        "country": cells[start + 6],
                        "timestamp": cells[start + 7],
                        "performance": cells[start + 8],
                        "product_key": cells[start + 9],
                        "windows_version": cells[start + 10],
                        "computer_name": cells[start + 11],
                        "parameter_change": cells[start + 12],
                    }
                )

            return activation_status
