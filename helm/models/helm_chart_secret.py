# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class HelmChartSecret(models.Model):
    _name = "helm.chart.secret"
    _description = "Helm Chart Secret"

    name = fields.Char()
    chart_id = fields.Many2one("helm.chart")
    release_id = fields.Many2one("helm.release")
    data_ids = fields.One2many("helm.chart.secret.data", "secret_id")
