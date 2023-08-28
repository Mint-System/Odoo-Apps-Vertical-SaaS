import logging, requests
from odoo import _, api, fields, models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class LicenseActivation(models.TransientModel):
    _name = 'license.activation'
    _description = 'License Activation'

    # @api.model
    # def default_get(self, fields):
    #     res = super(LicenseActivation, self).default_get(fields)
        
    #     if "default_partner_id" in self._context and "partner_id" not in fields:
    #         fields.append("partner_id")
    #     res["partner_id"] = self._context.get("default_partner_id")
    #     return res

    name = fields.Char(readonly=True)
    license_id = fields.Many2one('license.license')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        
        license_id = self._context['license_id']
        if license_id:
            license_id = self.env['license.license'].browse(license_id)
            self._get_activations(license_id)
            # self.sudo().create({
            #     'name': 'activation',
            #     'license_id': license_id.id
            # })

        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

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

    @api.model
    def _get_activations(self, license_id):

        edition_short = str(license_id.product_id.get_value_by_key('EditionShort'))

        if edition_short and license_id.name != _('New'):

            url = 'https://www.ocad.com/ocadintern/db_increaseCounter/getActivations_2018.php'
            params = {
                'edition': edition_short,
                'licenseNumber': license_id.name,
            }
            auth = (license_id.company_id.ocad_username, license_id.company_id.ocad_password)

            response = requests.get(url, params=params, auth=auth)
            
            _logger.warning(['params', params])
            _logger.warning(['response', response.text])