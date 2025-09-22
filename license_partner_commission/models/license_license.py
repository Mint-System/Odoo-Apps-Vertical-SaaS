import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = "license.license"

    referrer_id = fields.Many2one("res.partner", compute="_compute_referrer_id", store=True)

    @api.depends("sale_order_id", "sale_order_id.referrer_id")
    def _compute_referrer_id(self):
        for rec in self:
            if rec.sale_order_id:
                rec.referrer_id = rec.sale_order_id.referrer_id
            else:
                rec.referrer_id = False
