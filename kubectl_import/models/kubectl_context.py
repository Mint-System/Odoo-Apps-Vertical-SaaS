import logging

from odoo import _, models

from .ir_actions_client import display_notification

_logger = logging.getLogger(__name__)


class KubectlContext(models.Model):
    _inherit = "kubectl.context"

    def action_import_namespaces(self):
        self.ensure_one()
        result = self.env["kubectl.namespace"]._import_namespaces(self)
        return display_notification(_("Namespaces Imported"), result, "success")
