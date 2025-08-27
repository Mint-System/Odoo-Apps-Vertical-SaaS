import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Activate licenses and send license information mail if:
        - Order is from website
        - There is no order comment
        - The "license exists" option is not checked
        - Any order line is a license
        """
        res = super().action_confirm()

        for order in self:
            if not order.license_exists and any(order.order_line.mapped("is_license")) and not order.comment:
                # Activate licenses
                order.order_line.license_ids.action_activate()

                # Send mail with license information
                mail_template = self.env.ref("license_ocad_mail.mail_template_license_information")
                order.with_context(force_send=True).message_post_with_template(
                    mail_template.id,
                    composition_mode="comment",
                    email_layout_xmlid="mail.mail_notification_light",
                )

        return res
