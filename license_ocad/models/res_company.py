import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    ocad_username = fields.Char()
    ocad_password = fields.Char()
