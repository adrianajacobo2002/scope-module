from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleProposalAsset(models.Model):
    _name = "sale.proposal.asset"
    _description = "PDFs de propuesta técnica (Header/Footer)"
    _order = "type, id"

    team_id = fields.Many2one("crm.team", required=True, ondelete="cascade")
    type = fields.Selection([("header", "Header"), ("footer", "Footer")], required=True)
    name = fields.Char(required=True, default=lambda self: _("PDF"))
    file = fields.Binary(string="Archivo (PDF)", required=True, attachment=True)
    filename = fields.Char(string="Nombre archivo")

    _sql_constraints = [
        (
            "uniq_team_type",
            "unique(team_id, type)",
            "Ya existe un documento de ese tipo para este equipo.",
        )
    ]

    @api.constrains("file")
    def _check_pdf(self):
        for rec in self:
            if not rec.file:
                raise ValidationError(_("Debes subir un PDF."))
