import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LicenseType(models.Model):
    _name = "license.type"
    _description = "License Type"

    name = fields.Char()
