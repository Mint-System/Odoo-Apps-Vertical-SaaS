import logging, hashlib, random, requests
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

    # Existing fields
    client_order_ref = fields.Char(required=True)

    # New fields
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    download_token = fields.Char(compute='_compute_download_token', readonly=True, store=True, precompute=True)
    download_link = fields.Char(compute='_compute_download_link', readonly=True, store=True)
    registered = fields.Boolean(readonly=True)

    @api.depends('name')
    def _compute_download_token(self):
        char_table = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz' # 58 char
        for license in self:
            result = ''
            for _ in range(8):
                result += char_table[random.randint(0, 57)]  # randint includes both ends of the range
            license.download_token = result

    @api.depends('name', 'product_id', 'download_token')
    def _compute_download_link(self):
        """Generate download link."""
        for license in self:
            if license.product_id and license.name != _('New'):
                edition_short = str(license.product_id.get_value_by_key('EditionShort'))
                version = str(license.product_id.get_value_by_key('Version'))
                license.download_link = 'https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=' + edition_short + '&l=' + license.name + '&v=' + version + '&d=' + license.download_token

    @api.depends('name', 'product_id', 'partner_id', 'client_order_ref')
    def _compute_key(self):
        for license in self:
            if license.product_id and license.client_order_ref and license.name != _('New'):
                version = license.product_id.get_value_by_key('Version')
                edition_long = license.product_id.get_value_by_key('EditionLong')
                # Values: 2012, 5002, 'Mapping Solutions', 'OCAD AG'
                # Result: 5E27-8047-C507
                license.key = ''.join(get_ocad2018_checksum(version, int(license.name), edition_long, license.client_order_ref))

    def _create_license(self):
        message = ''
        for license in self:

            edition_short = license.product_id.get_value_by_key('EditionShort')
            number_of_activations = license.product_id.get_value_by_key('NumberOfActivations')
            is_team = license.product_id.get_value_by_key('IsTeam')

            url = 'https://www.ocad.com/ocadintern/db_newlicense/UpdateNewLicense2018.php'
            params = {
                'edition': edition_short,
                'licenseNumber': license.name,
                'checkSum': license.key,
                'dwnlink': license.download_token,
                'numberOfActivations': number_of_activations,
                'subBegin': license.date_start.strftime('yyyy/mm/dd'),
                'subEnd': license.date_end.strftime('yyyy/mm/dd'),
                'isTeam': is_team,
                'reseller': ''
            }
            auth = (self.company_id.ocad_username, self.company_id.ocad_password)

            response = requests.post(url, params=params, auth=auth)
            message += response.text + '\n'

        return message

    def _enable_license(self):
        message = ''
        for license in self:

            edition_short = license.product_id.get_value_by_key('EditionShort')

            url = 'https://www.ocad.com/ocadintern/db_increaseCounter/increaseCounter_2018.php'
            params = {
                'edition': edition_short,
                'licenseNumber': license.name,
            }
            auth = (self.company_id.ocad_username, self.company_id.ocad_password)

            response = requests.post(url, params=params, auth=auth)
            message += response.text + '\n'

        return message

    def _disable_license(self):
        message = ''
        for license in self:

            url = 'https://www.ocad.com/ocadintern/db_increaseCounter/deactivateActivation_2018.php'
            params = {
                'ProductKeyValue': '',
                'LicenseNumberValue': license.name,
                'StatusValue': 3,
                'IdValue': ''
            }
            auth = (self.company_id.ocad_username, self.company_id.ocad_password)

            response = requests.post(url, params=params, auth=auth)
            message += response.text + '\n'

        return message

    def _get_action_notification(self, message):
        notification_type = 'success'
        notification_sticky = False
        if 'FEHLER' in message or 'Unauthorized' in message:
            notification_type = 'danger'
            notification_sticky = True

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'OCAD License Service',
                'message': message,
                'sticky': notification_sticky,
                'type': notification_type,
                'next': {'type': 'ir.actions.act_window_close'},  # Refresh the form
            }
        }

    def action_activate(self):
        """Create and enable license."""
        super().action_activate()

        message = self._create_license()
        # message += self._enable_license()

        if not ('FEHLER' in message or 'Unauthorized' in message):
            self.write({'registered': True})

        return self._get_action_notification(message)

    # def action_reset(self):
    #     super().action_reset()
    #     for license in self:

    def action_disable(self):
        """Disable license."""
        super().action_disable()

        message = self._disable_license()

        return self._get_action_notification(message)

    def action_enable(self):
        """Create and enable license."""
        super().action_activate()

        message = self._enable_license()

        return self._get_action_notification(message)

    # def action_cancel(self):
    #     super().action_cancel()
    #     for license in self:

    # def action_draft(self):
    #     super().action_draft()
    #     for license in self:

    # def unlink(self):
    #     return super(License, self).unlink()