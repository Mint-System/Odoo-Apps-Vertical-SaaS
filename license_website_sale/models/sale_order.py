import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    licenses_already_exist = fields.Boolean(string="I already have an OCAD license/subscription", default=False)