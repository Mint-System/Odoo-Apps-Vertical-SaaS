import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class KubectlNamespace(models.Model):
    _name = "kubectl.namespace"
    _description = "Kubectl Namespace"
    _resource = "namespace"

    display_name = fields.Char(compute="_compute_display_name")

    name = fields.Char(required=True)

    cluster_id = fields.Many2one("kubectl.cluster", required=True)

    _sql_constraints = [
        (
            "unique_name_by_cluster_id",
            "UNIQUE(name, cluster_id)",
            "Namespace must be unique per cluster.",
        ),
    ]

    @api.model
    def get_or_create(self, values):
        namespace_id = self.search(
            [
                ("name", "=", values["name"]),
                ("cluster_id", "=", values["cluster_id"]),
            ]
        )
        if namespace_id:
            return namespace_id
        else:
            return self.create(values)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.cluster_id.name})"
