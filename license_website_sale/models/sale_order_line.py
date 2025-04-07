import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def create_license(self):
        """
        Create license only if "license exists" is not checked and
        no comment has been added to the sale order.
        """
        for line in self:
            if not line.order_id.license_exists and not line.order_id.comment:
                return super().create_license()
            else:
                return
