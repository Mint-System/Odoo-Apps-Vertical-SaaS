import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_license_values(self):
        """
        Add end date from subscription.
        """
        res = super()._prepare_license_values()
        res["date_start"] = self.order_id.start_date
        res["date_end"] = self.order_id.next_invoice_date
        return res

    def _get_renew_upsell_values(self, subscription_management, period_end=None):
        """
        Link licenses to the new sale order line.
        """
        order_lines = super()._get_renew_upsell_values(subscription_management, period_end)
        res = []
        for order_line in order_lines:
            parent_line_id = self.browse(order_line[2]["parent_line_id"])
            order_line[2]["license_ids"] = parent_line_id.license_ids
            order_line[2]["discount"] = parent_line_id.discount
            parent_line_id.license_ids.parent_sale_line_id = parent_line_id
            res.append(order_line)
        return res

    def _compute_discount(self):
        """
        The _compute_discount method in sale_subscription/models/sale_order_line.py removes lines from super calls.
        This method copies the functionality of sale_order_line_pricelist_fixed_discount.
        """

        super()._compute_discount()

        for line in self:
            parent_sale_line_id = line.license_ids[0].parent_sale_line_id if line.license_ids else False

            # Read filter date from context
            date = self._context.get("date") or line.order_id.commitment_date or line.order_id.date_order

            # Apply fixed price discount
            discount = line.order_id.pricelist_id._get_percent_price(line.product_id, line.product_uom_qty, date)

            if discount:
                line.discount = discount

            elif parent_sale_line_id and line.product_uom_qty == 1.0 and len(self) >= 2:
                line.discount = parent_sale_line_id.discount
