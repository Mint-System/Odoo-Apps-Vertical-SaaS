import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_license = fields.Boolean(compute="_compute_is_license", store=True)
    license_ids = fields.One2many("license.license", "sale_line_id")
    license_refs = fields.Char(compute="_compute_license_refs")
    license_count = fields.Integer(compute="_compute_license_count")

    def _compute_license_count(self):
        for line in self:
            line.license_count = len(line.license_ids)

    @api.depends("product_id")
    def _compute_is_license(self):
        for rec in self:
            rec.is_license = rec.product_id.license_ok

    @api.depends("license_ids")
    def _compute_license_refs(self):
        for rec in self:
            rec.license_refs = ", ".join(rec.license_ids.mapped("client_order_ref"))

    def _create_license(self):
        """
        Create single license and bump ordered qty.
        """
        self.ensure_one()
        if not isinstance(self.id, models.NewId) and self.state in ["sale"] and self.is_license:
            value = self._prepare_license_values()
            license = self.env["license.license"].sudo().create(value)
            license_msg = _("This license has been created from: %s (%s)") % (
                self.order_id._get_html_link(),
                self.product_id.name,
            )
            license.message_post(body=license_msg)

            # Adjust so line qty
            if self.product_uom_qty < self.license_count:
                diff = self.license_count - self.product_uom_qty
                self.write({"product_uom_qty": self.product_uom_qty + diff})

    def create_licenses(self):
        """
        Create multiple licenses based on license policy.
        """
        for line in self.filtered(
            lambda r: not isinstance(r.id, models.NewId) and r.state in ["sale"] and r.is_license
        ):
            qty = line.product_uom_qty
            if line.product_id.license_ok:
                if not qty and line.product_id.license_policy == "quantity":
                    qty = line.product_uom_qty
                elif not qty and line.product_id.license_policy == "product":
                    qty = 1
                active_license_ids_count = len(
                    line.license_ids.filtered(lambda r: r.state in ["draft", "assigned", "active"])
                )
                count_new_licenses = int(qty) - active_license_ids_count

                for _qty in range(count_new_licenses):
                    values = line._prepare_license_values()
                    license = line.env["license.license"].sudo().create(values)
                    license_msg = _("This license has been created from: %s (%s)") % (
                        line.order_id._get_html_link(),
                        line.product_id.name,
                    )
                    license.message_post(body=license_msg)

    def _prepare_license_values(self):
        """
        Prepare values for license creation.
        """
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
            "client_order_ref": self.order_id.client_order_ref.strip(),
        }

    def button_create_license(self):
        self._create_license()
