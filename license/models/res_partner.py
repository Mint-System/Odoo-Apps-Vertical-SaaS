import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    license_ids = fields.One2many("license.license", "partner_id")
    license_count = fields.Integer(compute="_compute_license_count", store=True)

    @api.depends("license_ids")
    def _compute_license_count(self):
        for partner in self:
            partner.license_count = len(partner.license_ids)

    def action_view_license(self):
        self.ensure_one()
        view_form_id = self.env.ref("license.license_view_form").id
        view_tree_id = self.env.ref("license.license_view_tree").id
        action = {
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.license_ids.ids)],
            "view_mode": "tree,form",
            "name": _("Licenses"),
            "res_model": "license.license",
        }
        if self.license_count == 1:
            action.update(
                {"views": [(view_form_id, "form")], "res_id": self.license_ids.id}
            )
        else:
            action["views"] = [(view_tree_id, "tree"), (view_form_id, "form")]
        return action
