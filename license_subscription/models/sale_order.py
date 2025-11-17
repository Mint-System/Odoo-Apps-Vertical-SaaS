import logging
from datetime import timedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    next_invoice_date = fields.Date(inverse="_inverse_next_invoice_date")

    def _inverse_next_invoice_date(self):
        for order in self:
            order.order_line.filtered(lambda line: line.is_license).license_ids.filtered(
                lambda license: license.date_end != order.next_invoice_date
            ).write({"date_end": order.next_invoice_date})

    def action_confirm(self):
        """
        When confirmation happens after start date, set next invoice date to today.
        """
        res = super().action_confirm()
        today = fields.Date.today()
        if today > self.start_date:
            self.next_invoice_date = today
        return res

    def _prepare_upsell_renew_order_values(self, subscription_management):
        """
        If start date of renewal is a past date, ensure that the next invoice date is
        today.
        """
        res = super()._prepare_upsell_renew_order_values(subscription_management)
        today = fields.Date.today()
        if res["start_date"] < today:
            res["last_invoice_date"] = today
            res["next_invoice_date"] = today
        return res

    def _prepare_renew_upsell_order(self, subscription_management, message_body):
        """
        Ensure the renewal is valid until 5 days after next invoice date.
        Update the prices of the renewal order.
        """
        action = super()._prepare_renew_upsell_order(subscription_management, message_body)
        new_order = self.env["sale.order"].browse(action["res_id"])
        if new_order:
            new_order.write({"validity_date": self.next_invoice_date + timedelta(days=5)})
            new_order.action_update_prices()  # When prices are updated the link to parent lines are lost
        return action

    def _action_cancel(self):
        """
        Link licenses with previous sale order lines.
        """
        for license in self.order_line.license_ids.filtered(lambda r: r.parent_sale_line_id):
            license.write(
                {
                    "sale_line_id": license.parent_sale_line_id.id,
                }
            )
        return super()._action_cancel()

    def unlink(self):
        """
        Link licenses with previous sale order lines.
        """
        for license in self.order_line.license_ids.filtered(lambda r: r.parent_sale_line_id):
            license.write({"sale_line_id": license.parent_sale_line_id.id})
        return super().unlink()
