import logging

from odoo import api, fields, models
from odoo.tools.date_utils import get_timedelta

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    end_date = fields.Date(
        compute="_compute_end_date", inverse="_inverse_end_date", store=True
    )

    @api.depends("recurrence_id")
    def _compute_end_date(self):
        for order in self:
            order.end_date = order.start_date + get_timedelta(
                order.recurrence_id.duration, order.recurrence_id.unit
            )

    def _inverse_end_date(self):
        for order in self:
            order.order_line.filtered(lambda line: line.is_license).license_ids.write(
                {"date_end": order.end_date}
            )

    def _prepare_renew_upsell_order(self, subscription_management, message_body):
        """Link existing licenses to new sale order lines."""
        action = super()._prepare_renew_upsell_order(
            subscription_management, message_body
        )
        new_order = self.env["sale.order"].browse(action["res_id"])
        if new_order:
            for line in new_order.order_line:
                line.parent_line_id.license_ids.write({"sale_line_id": line.id})
        return action
