import logging
import uuid
from odoo import _, api, fields, models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'license.license'
    _description = 'License'

    name = fields.Char(default=lambda self: _('New'), required=True, readonly=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    key = fields.Char(default=lambda self: _('New'), compute='_compute_key', tracking=True, required=True, store=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    type_id = fields.Many2one('license.type', readonly=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.product', tracking=True, readonly=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('assigned', 'Assigned'),
            ('active', 'Active'),
            ('disabled', 'Disabled'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled')
        ],
        tracking=True,
        string='Status',
        copy=False,
        default='draft')
    date_start = fields.Date()
    date_end = fields.Date()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('license.license') or _('New')
        return super().create(vals_list)

    @api.depends('create_date')
    def _compute_key(self):
        for license in self.filtered(lambda l: l.key == _('New')):
            license.key = str(uuid.uuid4()).upper()

    def action_assign(self):
        for license in self:
            if not license.partner_id:
                raise UserError(
                    _("You cannot assign a license if no partner is set.")
                )
            license.write({'state': 'assigned'})

    def action_activate(self):
        for license in self:
            license.write({
                'state': 'active',
                'date_start': fields.Datetime.now()
            })

    def action_reset(self):
        for license in self:
            license.write({
                'state': 'assigned',
                'date_start': False,
                'date_end': False
            })

    def action_disable(self):
        for license in self:
            license.write({
                'state': 'disabled',
                'date_end': fields.Datetime.now()
            })

    def action_cancel(self):
        for license in self:
            license.write(
                {'state': 'cancelled',
                'date_end': fields.Datetime.now()
            })

    def action_draft(self):
        for license in self:
            license.write({
                'state': 'draft',
                'date_start': False,
                'date_end': False
            })

    def _can_be_deleted(self):
        self.ensure_one()
        return self.state in ['draft', 'cancelled']

    def unlink(self):
        for license in self:
            if not license._can_be_deleted():
                raise UserError(
                    _("You cannot delete a licnese which is not draft or cancelled.")
                )
        return super(License, self).unlink()