import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_license = fields.Boolean(compute="_compute_is_license", store=True)
    license_ids = fields.Many2one("license.license", "sale_line_id")

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id")
    def _compute_amount(self):
        res = super()._compute_amount()
        for line in self.filtered(lambda l: not isinstance(l.id, models.NewId) and l.state in ['sale', 'done'] and (l.product_uom_qty > l.order_id.license_count)):
            line._create_license(qty=line.product_uom_qty-line.order_id.license_count)
        return res

    @api.depends("product_id")
    def _compute_is_license(self):
        for rec in self:
            rec.is_license = rec.product_id.license_ok

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        for line in lines.filtered(lambda l: l.order_id.state == 'sale'):
            line._create_license()
        return lines
    
    def _create_license_prepare_values(self):
        self.ensure_one()
        if not self.order_id.client_order_ref:
            raise UserError(_("Cannot create license without customer reference."))
        return {
            "partner_id": self.order_id.partner_id.id,
            "product_id": self.product_id.id,
            "type_id": self.product_id.license_type_id.id,
            "sale_line_id": self.id,
            "sale_order_id": self.order_id.id,
            "state": "assigned",
            "client_order_ref": self.order_id.client_order_ref,
        }

    def _create_license(self, qty=None):
        """Create a license based on policy."""

        if not qty and self.product_id.license_policy == "quantity":
            qty = self.product_uom_qty
        elif not qty and self.product_id.license_policy == "product":
            qty = 1

        for _qty in range(int(qty)):
            values = self._create_license_prepare_values()
            license = self.env["license.license"].sudo().create(values)
            license_msg = _("This license has been created from: %s (%s)") % (
                self.order_id._get_html_link(),
                self.product_id.name,
            )
            license.message_post(body=license_msg)
        return True
