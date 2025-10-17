import logging

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class HelmRelease(models.Model):
    _inherit = "helm.release"

    sale_line_ids = fields.One2many("sale.order.line", "release_id")

    def _eval_value(self, expression):
        """
        Add order_id to context.
        """

        order_id = self.sale_line_ids[0].order_id if self.sale_line_ids else False
        if order_id:
            return safe_eval(expression, {"self": self, "release": self, "order_id": order_id})
        else:
            return super()._eval_value(expression)
