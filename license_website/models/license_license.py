from odoo import _, api, fields, models
from werkzeug.urls import url_join
import logging
_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = ['license.license', 'portal.mixin']
    _name = 'license.license'

    def action_preview_license(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': url_join(self.get_base_url(), '/my/license/%s' % self.id),
        }