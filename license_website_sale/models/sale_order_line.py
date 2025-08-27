import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def create_licenses(self):
        # Only proceed if none of the orders have license_exists or comment
        orders = self.order_id
        if any(order.license_exists or bool(order.comment) for order in orders):
            return False
        return super().create_licenses()
