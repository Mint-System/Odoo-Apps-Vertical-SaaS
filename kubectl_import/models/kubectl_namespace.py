import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class KubectlNamespace(models.Model):
    _inherit = "kubectl.namespace"

    uid = fields.Char(readonly=True)

    def _get_uid(self):
        """
        Get uid of the record
        """
        for rec in self.filtered(lambda r: not r.uid):
            command = f"kubectl get {self._resource} {rec.name} -o jsonpath='{{.metadata.uid}}'"
            response = rec
            rec.uid = response

    @api.model
    def _import_namespaces(self, context_id):
        """
        Load all namespaces from the current context.
        Creat missing namespace entries.
        """
        cluster_id = context_id.cluster_id
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
