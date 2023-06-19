from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class License(models.Model):
    _name = 'license.license'
    _description = 'License'

    name = fields.Char()
    value = fields.Char()
    type_id = fields.Many2one('license.type')