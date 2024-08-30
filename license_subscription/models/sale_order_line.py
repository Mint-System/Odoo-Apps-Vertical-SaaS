import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_license_values(self):
        """Add end date from subscription."""
        res = super()._prepare_license_values()
        res["date_end"] = self.order_id.next_invoice_date
        return res
