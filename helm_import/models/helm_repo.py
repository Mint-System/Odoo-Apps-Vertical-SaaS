import logging
import json

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
            # "next": {
            #     "type": "ir.actions.client",
            #     "tag": "reload",
            # },
        },
    }


class HelmRepo(models.Model):
    _inherit = "helm.repo"

    def action_import_charts(self):
        self.ensure_one()
        command = f"helm search repo {self.name} --output json".split(" ")
        result = self._run(command)
        data = json.loads(result.stdout)
        _logger.warning(data)
        for item in data:
            name = item["name"].split("/")[1]
            chart_id = self.env["helm.chart"].search([("name", "=", name), ("repo_id", "=", self.id)])
            if not chart_id:
                self.env["helm.chart"].create({"name": name, "repo_id": self.id})
        return display_notification(_("Charts Imported"), result, "success")
