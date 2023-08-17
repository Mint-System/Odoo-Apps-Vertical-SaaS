import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    ocad_username = fields.Char()
    ocad_password = fields.Char()
