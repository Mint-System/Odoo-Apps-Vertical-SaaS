from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class LicenseType(models.Model):
    _name = 'license.type'
    _description = 'License Type'

    name = fields.Char()
