import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = "license.license"

    sale_line_id = fields.Many2one(
        "sale.order.line",
        string="Sales Order Item",
        tracking=True,
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
        readonly=True,
        states={"draft": [("readonly", False)], "assigned": [("readonly", False)]},
    )
    partner_id = fields.Many2one(compute="_compute_partner_id", store=True, copy=True)
    product_id = fields.Many2one(
        compute="_compute_product_id",
        store=True,
        copy=True,
        domain=[("license_ok", "=", True)],
    )

    @api.depends("sale_order_id", "sale_order_id.partner_id")
    def _compute_partner_id(self):
        for rec in self:
            if rec.sale_order_id:
                rec.partner_id = rec.sale_order_id.partner_id

    @api.depends("sale_line_id", "sale_line_id.product_id")
    def _compute_product_id(self):
        for rec in self:
            if rec.sale_line_id:
                rec.product_id = rec.sale_line_id.product_id

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
