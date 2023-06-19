from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    license_ids = fields.Many2many('license.license', compute='_compute_license_ids', string='Licenses associated to this sale')
    license_count = fields.Integer(string='Licenses', compute='_compute_license_ids', groups='license.group_user')

    @api.depends('order_line.product_id')
    def _compute_license_ids(self):
        for order in self:
            order.license_ids = self.env['license.license'].search([('sale_line_id', 'in', order.order_line.ids), ('sale_order_id', '=', order.id)])
            order.license_count = len(order.license_ids)

    def action_view_license(self):
        self.ensure_one()
        view_form_id = self.env.ref('license.license_view_form').id
        view_tree_id = self.env.ref('license.license_view_tree').id
        action = {
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.license_ids.ids)],
            'view_mode': 'tree,form',
            'name': _('Licenses'),
            'res_model': 'license.license',
        }
        if len(self.license_ids) == 1:
            action.update({'views': [(view_form_id, 'form')], 'res_id': self.license_ids.id})
        else:
            action['views'] = [(view_tree_id, 'tree'), (view_form_id, 'form')]
        return action

    def _action_confirm(self):
        """On SO confirmation, some lines should generate a license."""
        res = super()._action_confirm()
        for line in self.order_line.filtered(lambda l: l.is_license):
            line._create_license()
        return res

    def _action_cancel(self):
        """On SO cancel, set related state on linked licenses."""
        self.license_ids.write({'state': 'cancelled'})
        return super()._action_cancel()