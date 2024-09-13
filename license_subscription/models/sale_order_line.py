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

    # def _get_renew_upsell_values(self, subscription_management, period_end=None):
    #     """
    #     Pass parent line discount.
    #     """
    #     order_lines = super()._get_renew_upsell_values(subscription_management, period_end)
    #     for order_line in order_lines:
    #         # (0, 0, {'parent_line_id': 45, 'temporal_type': 'subscription', 'product_id': 36, 'product_uom': 1, 'product_uom_qty': 1.0, 'price_unit': 80.0})
    #         parent_line_id = self.browse(order_line[2]['parent_line_id'])
    #         order_line[2]['discount'] = parent_line_id.discount
    #     return order_lines
