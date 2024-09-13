import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _send_order_confirmation_mail(self):
        """
        Activate licenses when bought throught shop before sending confirmation mail.
        """
        res = super()._send_order_confirmation_mail()

        for order in self:
            if order.website_id and any(order.order_line.mapped("is_license")):

                # Create licenses
                order.order_line.update_license()

                if not order.licenses_already_exist:

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

        return res
