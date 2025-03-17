import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_license_values(self):
        """
        Add end date from subscription.
        Link licenses to the new sale order line
        """
        res = super()._prepare_license_values()
        res["date_start"] = self.order_id.start_date
        res["date_end"] = self.order_id.next_invoice_date
        return res

    def _get_renew_upsell_values(self, subscription_management, period_end=None):
        """
        Add end date from subscription.
        Link licenses to the new sale order line
        """
        order_lines = super()._get_renew_upsell_values(subscription_management, period_end)

        # Add discount2 and link licenses to the new sale order line
        res = []
        for order_line in order_lines:
            parent_line_id = self.browse(order_line[2]["parent_line_id"])
            order_line[2]["discount2"] = parent_line_id.discount2
            order_line[2]["license_ids"] = parent_line_id.license_ids
            parent_line_id.license_ids.parent_sale_line_id = parent_line_id
            res.append(order_line)
        return res
