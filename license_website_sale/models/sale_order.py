import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    license_exists = fields.Boolean(
        help="Mark this option if you already own a OCAD license/subscription.",
        default=False,
    )
