import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = "license.license"

    parent_sale_line_id = fields.Many2one(
        "sale.order.line",
        string="Parent Sales Order Item",
        readonly=True,
    )
    sale_line_id = fields.Many2one("sale.order.line", inverse="_inverse_sale_line_id")

    def _inverse_sale_line_id(self):
        """Fallback to parent line if removed."""
        for rec in self:
            if not rec.sale_line_id and rec.parent_sale_line_id:
                rec.sale_line_id = rec.parent_sale_line_id
