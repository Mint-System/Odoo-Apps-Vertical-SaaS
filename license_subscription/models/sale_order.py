import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    next_invoice_date = fields.Date(inverse="_inverse_next_invoice_date")

    def _inverse_next_invoice_date(self):
        for order in self:
            order.order_line.filtered(lambda line: line.is_license).license_ids.write(
                {"date_end": order.next_invoice_date}
            )

    def _prepare_renew_upsell_order(self, subscription_management, message_body):
        """
        Update prices for existing and parent lines.
        """
        action = super()._prepare_renew_upsell_order(subscription_management, message_body)
        new_order = self.env["sale.order"].browse(action["res_id"])
        if new_order:
            new_order.write({"validity_date": self.next_invoice_date})
            # new_order.write({"comment": self.comment})

            # When prices are updated the link to parent lines is broken
            # Update the prices for this order and new order
            new_order.action_update_prices()

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
