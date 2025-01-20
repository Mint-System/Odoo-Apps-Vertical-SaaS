import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _send_order_confirmation_mail(self):
        res = super()._send_order_confirmation_mail()
        self.action_send_license_information()
        return res

    def action_send_license_information(self):
        """
        Activate licenses and send license information mails.
        """
        for order in self:
            if not order.license_exists and any(order.order_line.mapped("is_license")):

                # Update licenses
                order.order_line.update_license()

                # Activate licenses
                order.order_line.license_ids.action_activate()

                # Send mail with license information
                mail_template = self.env.ref(
                    "license_ocad_mail.mail_template_license_information"
                )
                order.with_context(force_send=True).message_post_with_template(
                    mail_template.id,
                    composition_mode="comment",
                    email_layout_xmlid="mail.mail_notification_light",
                )
