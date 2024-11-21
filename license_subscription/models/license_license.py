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
