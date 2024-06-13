import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = "license.license"

    sale_line_id = fields.Many2one(
        "sale.order.line",
        string="Sales Order Item",
        copy=False,
        domain="[('is_license', '=', True), ('state', 'in', ['sale', 'done']), ('order_partner_id', '=?', partner_id)]",
    )
    sale_order_id = fields.Many2one(
        string="Sales Order",
        related="sale_line_id.order_id",
        store=True,
        help="Sales order to which the license is linked.",
    )
    client_order_ref = fields.Char(
        string="Customer Reference",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    def action_view_so(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "name": _("Sales Order"),
            "views": [[False, "form"]],
            "context": {"create": False, "show_sale": True},
            "res_id": self.sale_order_id.id,
        }
        return action
