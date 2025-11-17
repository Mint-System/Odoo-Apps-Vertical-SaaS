import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_id = fields.Many2one(comodel_name="res.partner")

    license_ids = fields.Many2many(
        "license.license", compute="_compute_license_ids", string="Licenses associated to this sale", store=True
    )
    license_count = fields.Integer(
        string="Licenses", compute="_compute_license_ids", groups="license.group_user", store=True
    )

    @api.depends("order_line.product_id", "order_line.license_ids")
    def _compute_license_ids(self):
        for order in self:
            order.license_ids = self.env["license.license"].search(
                [
                    ("sale_line_id", "in", order.order_line.ids),
                    ("sale_order_id", "=", order.id),
                ]
            )
            order.license_count = len(order.license_ids)

    def action_confirm(self):
        res = super().action_confirm()
        self.order_line.create_licenses()
        return res

    def action_view_license(self):
        self.ensure_one()
        view_form_id = self.env.ref("license.license_view_form").id
        view_tree_id = self.env.ref("license.license_view_tree_editable").id
        action = {
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.license_ids.ids)],
            "view_mode": "list,form",
            "name": _("Licenses"),
            "res_model": "license.license",
        }
        if len(self.license_ids) == 1:
            action.update({"views": [(view_form_id, "form")], "res_id": self.license_ids.id})
        else:
            action["views"] = [(view_tree_id, "list"), (view_form_id, "form")]
        return action
