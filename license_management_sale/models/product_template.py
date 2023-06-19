from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = "product.template"

    license_ok = fields.Boolean(
        'Can be licensed',
        help='If set, confirming a sale order with this product will create a license.')
