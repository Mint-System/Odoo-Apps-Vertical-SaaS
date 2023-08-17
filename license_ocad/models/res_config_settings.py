import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ocad_username = fields.Char(related='company_id.ocad_username', readonly=False)
    ocad_password = fields.Char(related='company_id.ocad_password', readonly=False)
