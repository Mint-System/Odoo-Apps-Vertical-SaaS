import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


def display_notification(title, message, type):
    return {
        "type": "ir.actions.client",
        "tag": "display_notification",
        "params": {
            "title": title,
            "type": type,
            "message": message,
            "next": {
                "type": "ir.actions.client",
                "tag": "reload",
            },
        },
    }


class KubectlContext(models.Model):
    _inherit = "kubectl.context"

    def action_import_namespaces(self):
        self.ensure_one()
        result = self.env["kubectl.namespace"]._import_namespaces(self)
        return display_notification(_("Namespaces Imported"), result, "success")
