import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_license = fields.Boolean(compute="_compute_is_license", store=True)
    license_ids = fields.One2many("license.license", "sale_line_id")
    active_license_ids_count = fields.Integer(
        compute="_compute_active_license_ids_count"
    )

    def _compute_active_license_ids_count(self):
        for line in self:
            line.active_license_ids_count = len(
                self.license_ids.filtered(
                    lambda l: l.state in ["draft", "assigned", "active"]
                )
            )

    @api.depends("product_id")
    def _compute_is_license(self):
        for rec in self:
            rec.is_license = rec.product_id.license_ok

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id")
    def _compute_amount(self):
        """Create a license when order is confirmed or when amount of line is updated."""
        res = super()._compute_amount()
        for line in self.filtered(
            lambda l: not isinstance(l.id, models.NewId) and l.state in ["sale", "done"]
        ):
            line._create_license(qty=line.product_uom_qty)
        return res

    def _create_license_prepare_values(self):
        """Prepare values for license creation."""
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
        self.ensure_one()

        if not qty and self.product_id.license_policy == "quantity":
            qty = self.product_uom_qty
        elif not qty and self.product_id.license_policy == "product":
            qty = 1
        count_new_licenses = int(qty) - self.active_license_ids_count
        # _logger.warning([qty, self.active_license_ids_count, count_new_licenses])

        for _qty in range(count_new_licenses):
            values = self._create_license_prepare_values()
            license = self.env["license.license"].sudo().create(values)
            license_msg = _("This license has been created from: %s (%s)") % (
                self.order_id._get_html_link(),
                self.product_id.name,
            )
            license.message_post(body=license_msg)
        return True
