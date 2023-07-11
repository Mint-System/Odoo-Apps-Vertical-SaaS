from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
import uuid


class License(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'license.license'
    _description = 'License'

    name = fields.Char(default=lambda self: _('New'), readonly=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    key = fields.Char(compute='_compute_key', tracking=True, store=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    type_id = fields.Many2one('license.type', readonly=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', tracking=True, readonly=True, states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})
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
        for rec in self.filtered(lambda l: not l.key):
            rec.key = str(uuid.uuid4()).upper()

    def assign(self):
        for rec in self:
            rec.write({'state': 'assigned'})
