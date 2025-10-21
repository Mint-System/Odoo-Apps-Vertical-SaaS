# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class HelmChartSecret(models.Model):
    _name = "helm.chart.secret"
    _description = "Helm Chart Secret"

    name = fields.Char()

    chart_id = fields.Many2one("helm.chart", ondelete="cascade")
    release_id = fields.Many2one("helm.release", ondelete="cascade")
    data_ids = fields.One2many("helm.chart.secret.data", "secret_id")

    def copy(self, default=None):
        new_secret = super().copy(default=default)
        for data in self.data_ids:
            data.copy({"secret_id": new_secret.id})
        return new_secret

    def action_show_details(self):
        self.ensure_one()
        view = self.env.ref("helm.helm_chart_secret_form_view")
        return {
            "name": _("Secret Data"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "helm.chart.secret",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
        }
