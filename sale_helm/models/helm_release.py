import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HelmRelease(models.Model):
    _inherit = "helm.release"

    sale_line_ids = fields.One2many("sale.order.line", "release_id")

    def _eval_with_context(self, expression, context):
        """
        Add order_id to context.
        """
        if "order_id" in expression and "order_id" not in context:
            return False
        context["order_id"] = self.sale_line_ids[0].order_id if self.sale_line_ids else False
        return super()._eval_with_context(expression, context)
