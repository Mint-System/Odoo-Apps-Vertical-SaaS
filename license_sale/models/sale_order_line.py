import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_license = fields.Boolean(compute='_compute_is_license', store=True)
    license_ids = fields.Many2one('license.license', 'sale_line_id')

    @api.depends('product_id')
    def _compute_is_license(self):
        for rec in self:
            rec.is_license = rec.product_id.license_ok

    def _create_license_prepare_values(self):
        self.ensure_one()
        return {
            'partner_id': self.order_id.partner_id.id,
            'product_id': self.product_id.id,
            'type_id': self.product_id.license_type_id.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'state': 'assigned',
            'client_order_ref': self.order_id.client_order_ref # or self.order_id.partner_id.commercial_partner_id.name
        }

    def _create_license(self):
        """Create a license based on policy."""

        product_uom_qty = 1
        if self.product_id.license_policy == 'quantity':
            product_uom_qty = self.product_uom_qty
        for qty in range(int(product_uom_qty)):
            values = self._create_license_prepare_values()
            license = self.env['license.license'].sudo().create(values)
            license_msg = _('This license has been created from: %s (%s)', self.order_id._get_html_link(), self.product_id.name)
            license.message_post(body=license_msg)
        return True