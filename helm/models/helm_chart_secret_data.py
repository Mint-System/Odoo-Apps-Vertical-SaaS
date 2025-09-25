# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HelmChartSecretData(models.Model):
    _name = "helm.chart.secret.data"
    _description = "Helm Chart Secret Data"

    key = fields.Char(required=True)
    value = fields.Char(required=True)
    secret_id = fields.Many2one("helm.chart.secret", required=True)
