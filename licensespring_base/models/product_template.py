from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    licensespring_enable = fields.Boolean()
    licensespring_id = fiels.Integer()
    product_code = fields.Char()
    has_trial_period = fields.Boolean()
    trial_period_days = fiels.Integer()

    # def create

    # def write

    # def unlink

    # def _archive_product