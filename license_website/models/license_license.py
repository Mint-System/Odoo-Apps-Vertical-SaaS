import logging

from odoo import models

_logger = logging.getLogger(__name__)


class License(models.Model):
    _inherit = ["license.license", "portal.mixin"]
    _name = "license.license"

    def _compute_access_url(self):
        for record in self:
            record.access_url = "/my/licenses/{}".format(record.id)

    def action_preview_license(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": self.get_portal_url(),
        }
