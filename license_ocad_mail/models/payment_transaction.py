import logging

from odoo import models

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _finalize_post_processing(self):
        """
        Send license information.
        """
        res = super()._finalize_post_processing()
        for res in self:
            res.sale_order_ids.action_send_license_information()
        return res
