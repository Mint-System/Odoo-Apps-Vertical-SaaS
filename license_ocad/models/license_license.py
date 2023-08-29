import logging, hashlib, random, requests
from odoo import _, api, fields, models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)
from . import ocad


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
            if license.product_id and license.client_order_ref and license.name != _('New') and isinstance(license.name, int):
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

        if not ('FEHLER' in message or 'Unauthorized' in message):
            self.write({'registered': True})

        return self._get_action_notification(message)

    # def action_reset(self):
    #     super().action_reset()
    #     for license in self:

    # def action_disable(self):
    #     """Disable license."""
    #     super().action_disable()

    #     message = self._disable_license()

    #     return self._get_action_notification(message)

    # def action_enable(self):
    #     """Create and enable license."""
    #     super().action_activate()

    #     message = self._enable_license()

    #     return self._get_action_notification(message)

    # def action_cancel(self):
    #     super().action_cancel()
    #     for license in self:

    # def action_draft(self):
    #     super().action_draft()
    #     for license in self:

    # def unlink(self):
    #     return super(License, self).unlink()

    def action_view_activations(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'license.activation',
            'name': _('License Activations'),
            'view_mode': 'tree',
            'views': [[False, 'list']],
            'context': {'license_id': self.id},
            'domain': [('license_id', '=', self.id)],
        }
