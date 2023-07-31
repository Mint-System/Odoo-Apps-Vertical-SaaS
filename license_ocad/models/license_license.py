import logging
import hashlib
from odoo import _, api, fields, models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

# Get hash string
def hash_of_string(s):
    return hashlib.sha1(s.encode('utf-16-le')).hexdigest().upper()

# Convert hex to integer
def hex_to_int(s):
    hx = 0
    s = s.upper()
    slist = list(s)
    for c in slist:
        hx = hx*16 
        if (c in ['0','1','2','3','4','5','6','7','8','9']):
            hx = hx + ord(c) - ord('0')
        else:
            hx = hx + ord(c) - ord('A') + 10
        # print(c+" .. "+ str(hx)  +"--- "+ str(ord(c)) )
    return hx

# Get key byte
def pkv_get_key_byte(seed, a, b, c): 
    a = a % 25
    b = b % 3
    if (a % 2 == 0):
        return ((seed >> a) & 11111111) ^ ((seed >> b) | c)
    else:
        return ((seed >> a) & 11111111) ^ ((seed >> b) & c)

# Get OCAD2018 checksum
def get_ocad2018_checksum(v, lnum, e, lname): 

    slist = list(e)
    checksum = list('____-____-____')

        
    for i in [5, 6, 7, 8, 10, 11]:
        slist = list(hash_of_string(''.join(slist).upper() + lname.upper() + str(lnum) + lname.upper()))
        # print(''.join(slist))
        idx = (v*(i+1)+lnum) % 40
        # print(idx)
        checksum[i] = slist[idx]

    # print(checksum)

    s = checksum[5] + checksum[6] + checksum[7] + checksum[8] + checksum[10] + checksum[11]
    # print(s)
    a = pkv_get_key_byte(hex_to_int(s), lnum % 256, v % 2000, 13)
    # a = pkv_get_key_byte(8406981, ln % 256, v % 2000, 13)
    sl = list('{0:02X}'.format(a))
    checksum[12] = sl[0]
    checksum[13] = sl[1]
    # print(checksum)

    s = ''.join(checksum).replace('_', '')
    s = s.replace("-", "")

    slist = list(s)
    # print(s)

    slist = list(hash_of_string(e + ''.join(slist).upper() + str(lnum) + lname.upper()))
    checksum[0] = slist[8]
    checksum[1] = slist[23]
    checksum[2] = slist[12]
    checksum[3] = slist[16]
    # print(checksum)
    return checksum


class License(models.Model):
    _inherit = 'license.license'

    # Set partner_id to required and disallow editing in assigned state

    name = fields.Char(default=lambda self: _('New'), required=True, readonly=True, states={'draft': [('readonly', False)]})
    key = fields.Char(default=lambda self: _('New'), compute='_compute_key', tracking=True, required=True, store=True, states={'draft': [('readonly', False)]})
    type_id = fields.Many2one('license.type', readonly=True, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', required=True, tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.product', tracking=True, readonly=True, states={'draft': [('readonly', False)]})

    @api.depends('name', 'product_id', 'partner_id')
    def _compute_key(self):
        for license in self:
            if license.product_id:
                try:
                    version = license.product_id.get_value_by_key('Version')
                    edition_long = license.product_id.get_value_by_key('EditionLong')
                    # Values: 2012, 5002, 'Mapping Solutions', 'OCAD AG'
                    # Result: 5E27-8047-C507
                    license.key = ''.join(get_ocad2018_checksum(version, int(license.name), edition_long, license.partner_id.name))
                except Exception as error:
                    raise UserError(
                        _('Generating checksum failed with error: %s\n') % str(error) +
                        _('This is most likely due to missing product informations.')    
                    )

    def action_assign(self):
        super().action_assign()
        for license in self:
            _logger.warning({
                'warning': {
                    'title': _('Notification'),
                    'message': _('License assigned.'),
                    'type': 'notification'
                }
            })

    def action_activate(self):
        super().action_activate()
        for license in self:
            _logger.warning({
                'warning': {
                    'title': _('Notification'),
                    'message': _('License activated.'),
                    'type': 'notification'
                }
            })

    def action_reset(self):
        super().action_reset()
        for license in self:
            _logger.warning({
                'warning': {
                    'title': _('Notification'),
                    'message': _('License resetted.'),
                    'type': 'notification'
                }
            })

    def action_disable(self):
        super().action_disable()
        for license in self:
            _logger.warning({
                'warning': {
                    'title': _('Notification'),
                    'message': _('License disabled.'),
                    'type': 'notification'
                }
            })

    def action_cancel(self):
        super().action_cancel()
        for license in self:
            _logger.warning({
                'warning': {
                    'title': _('Notification'),
                    'message': _('License cancelled.'),
                    'type': 'notification'
                }
            })

    def action_draft(self):
        super().action_draft()
        for license in self:
            _logger.warning({
                'warning': {
                    'title': _('Notification'),
                    'message': _('License set to draft.'),
                    'type': 'notification'
                }
            })

    def unlink(self):
        return super(License, self).unlink()