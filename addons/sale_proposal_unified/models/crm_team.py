from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = "crm.team"

    incluir_propuesta_tecnica = fields.Boolean(string="Incluir propuesta técnica")

    proposal_header_pdf = fields.Binary(string="Header")
    proposal_header_pdf_filename = fields.Char(string="Nombre Header PDF")
    proposal_footer_pdf = fields.Binary(string="Footer")
    proposal_footer_pdf_filename = fields.Char(string="Nombre Footer PDF")

    proposal_asset_ids = fields.One2many(
        "sale.proposal.asset",
        "team_id",
        string="Docs Propuesta",
    )

    @api.constrains("incluir_propuesta_tecnica")
    def _check_min_pdfs(self):
        for team in self:
            if not team.incluir_propuesta_tecnica:
                continue
            has_header = bool(
                team.proposal_asset_ids.filtered(lambda r: r.type == "header")
            ) or bool(team.proposal_header_pdf)
            has_footer = bool(
                team.proposal_asset_ids.filtered(lambda r: r.type == "footer")
            ) or bool(team.proposal_footer_pdf)
            if not has_header:
                raise ValidationError(_("Debe adjuntar el Header (PDF)."))
            if not has_footer:
                raise ValidationError(_("Debe adjuntar el Footer (PDF)."))
