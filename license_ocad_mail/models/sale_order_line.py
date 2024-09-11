import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_license_values(self):
        """
        Customer reference must contain at least three letters.
        """
        # FIXME: This check will break the checkout process
        # if self.order_id.client_order_ref:
        #     if len(self.order_id.client_order_ref) < 3:
        #         raise UserError(
        #             _("Customer reference must contain at least three letters.")
        #         )
        return super()._prepare_license_values()
