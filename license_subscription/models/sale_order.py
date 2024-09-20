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
        Link existing licenses to new sale order lines.
        Recaclulate prices from pricelist.
        """
        action = super()._prepare_renew_upsell_order(
            subscription_management, message_body
        )
        new_order = self.env["sale.order"].browse(action["res_id"])
        if new_order:
            new_order.write({"validity_date": self.next_invoice_date})
            for line in new_order.order_line:
                line.parent_line_id.license_ids.write({"sale_line_id": line.id})
                line._compute_price_unit()
        return action

    def _action_cancel(self):
        """
        Link licenses with previous sale order lines.
        """
        for order in self:
            for line in order.order_line.filtered(lambda l: l.parent_line_id):
                line.license_ids.write({"sale_line_id": line.parent_line_id.id})
        return super()._action_cancel()

    def unlink(self):
        """
        Link licenses with previous sale order lines.
        """
        for order in self:
            for line in order.order_line.filtered(lambda l: l.parent_line_id):
                line.license_ids.write({"sale_line_id": line.parent_line_id.id})
        return super().unlink()
