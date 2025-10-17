import logging
import subprocess

import yaml

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

from .ir_actions_client import display_notification

_logger = logging.getLogger(__name__)


class HelmRelease(models.Model):
    _name = "helm.release"
    _description = "Helm Release"

    name = fields.Char(help="Name of the release.", required=True)
    chart_id = fields.Many2one("helm.chart", help="Chart that shall be installed.", required=True)
    context_id = fields.Many2one("kubectl.context", help="Context used for installation.", required=True)
    cluster_id = fields.Many2one(related="context_id.cluster_id")
    create_namespace = fields.Boolean()
    namespace = fields.Char(help="Namespace with this input will be created.")
    namespace_id = fields.Many2one("kubectl.namespace", string="Linked Namespace", help="Target namespace in cluster.")
    partner_id = fields.Many2one("res.partner", string="Customer")
    state = fields.Selection(
        selection=[("draft", "Draft"), ("installed", "Installed")],
        default="draft",
    )
    output = fields.Text()
    value_ids = fields.One2many(
        "helm.chart.value",
        "release_id",
        string="Updatable values",
        help="These values can be changed.",
    )
    values = fields.Text(
        compute="_compute_values", store=True, help="Values computed from the chart and the release values."
    )
    ingress_url = fields.Char(compute="_compute_ingress_url")

    def _eval_value(self, expression):
        return safe_eval(expression, {"self": self, "release": self})

    @api.depends("chart_id", "chart_id.value_ids", "state")
    def _compute_values(self):
        """
        Evaluate custom values of the chart.
        """
        for release in self:
            if release.state == "draft" and release.chart_id.state == "added":
                dict_values = {}
                for value in release.chart_id.value_ids.filtered(
                    lambda v: not v.filter_cluster_ids or release.cluster_id in v.filter_cluster_ids
                ):
                    try:
                        new_value = release._eval_value(value.value)

                        # Apply to release field
                        if value.field_id:
                            release[value.field_id.name] = new_value

                        # Apply to path
                        if value.path:
                            dict_values[value.path] = new_value

                    except Exception as e:
                        _logger.error(f"Invalid expression {value.value}: {str(e)}")
                        # raise ValidationError(f"Invalid expression {value.value}: {str(e)}")
                try:
                    release.values = yaml.safe_dump(dict_values, sort_keys=False)
                except yaml.YAMLError as e:
                    raise ValidationError(f"Error converting to YAML: {str(e)}")

    def _compute_ingress_url(self):
        for release in self:
            if release.state == "installed" and release.namespace_id:
                release.ingress_url = "https://" + release.namespace_id.name + "." + release.cluster_id.domain
            else:
                release.ingress_url = ""

    def action_install(self):
        """
        Install the Helm chart using the current context configuration.
        """
        self.ensure_one()

        # Check if chart has been added
        if self.chart_id.state != "added":
            raise ValidationError(_(f"The chart '{self.chart_id.name}' has not been added."))

        try:
            command = ["helm", "install", self.name, f"{self.chart_id.repo_id.name}/{self.chart_id.name}"]
            if self.create_namespace:
                command += ["--create-namespace", "--namespace", self.namespace]
            result = self.context_id.run(command, self.values)
            if self.create_namespace and not self.namespace_id:
                self.namespace_id = self.env["kubectl.namespace"].create(
                    {"name": self.namespace, "cluster_id": self.cluster_id.id}
                )
            self.write({"state": "installed"})
            self.output = result.stdout
            return display_notification(_("Chart Installed"), result.stdout, "success")
        except subprocess.CalledProcessError as e:
            self.output = e.stderr
            return display_notification(_("Installing Chart Failed"), e.stderr, "danger")

    def action_upgrade(self):
        """
        Upgrade the Helm chart using the current context configuration.
        """
        self.ensure_one()
        try:
            result = self.context_id.run(
                [
                    "helm",
                    "upgrade",
                    self.name,
                    f"{self.chart_id.repo_id.name}/{self.chart_id.name}",
                ]
            )
            self.write({"state": "draft"})
            self.output = result.stdout
            return display_notification(_("Chart Upgraded"), result.stdout, "success")
        except subprocess.CalledProcessError as e:
            self.output = e.stderr
            return display_notification(_("Upgrading Chart Failed"), e.stderr, "danger")

    def action_uninstall(self):
        """
        Uninstall the Helm chart using the current context configuration.
        """
        self.ensure_one()
        try:
            result = self.context_id.run(
                [
                    "helm",
                    "uninstall",
                    self.name,
                ]
            )
            self.write({"state": "draft"})
            self.output = result.stdout
            return display_notification(_("Chart Uninstalled"), result.stdout, "success")
        except subprocess.CalledProcessError as e:
            self.output = e.stderr
            return display_notification(_("Uninstalling Chart Failed"), e.stderr, "danger")
