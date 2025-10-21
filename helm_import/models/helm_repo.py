import logging

from odoo import _, models

from ../../helm/models/ir_actions_client import display_notification

_logger = logging.getLogger(__name__)


class HelmRepo(models.Model):
    _inherit = "helm.repo"

    def action_import_charts(self):
        self.ensure_one()
        command = f"kubectl get {self._resource} -o json".split(" ")
        result = context_id.run(command)
        data = json.loads(result.stdout)
        for item in data["items"]:
            name = item["metadata"]["name"]
            uid = item["metadata"]["uid"]
            namespace_id = self.search([("name", "=", name), ("cluster_id", "=", cluster_id.id)])
            if namespace_id:
                namespace_id.write({"uid": uid})
            else:
                self.create({"name": name, "uid": uid, "cluster_id": cluster_id.id})
