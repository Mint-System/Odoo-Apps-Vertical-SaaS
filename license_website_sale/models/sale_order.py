import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _send_order_confirmation_mail(self):
        """Activate licenses when bought throught shop before sending confirmation mail."""
        if self.website_id and self.order_line and self.order_line.license_ids:
            self.order_line.license_ids.action_activate()
        return super()._send_order_confirmation_mail()
