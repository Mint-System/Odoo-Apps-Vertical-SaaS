import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def create_license(self):
        """
        Create license only if "license exists" is not checked.
        """
        for line in self:
            if not line.order_id.license_exists:
                return super().create_license()
            else:
                return
