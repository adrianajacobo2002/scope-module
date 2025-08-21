from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CrmTeam(models.Model):
    _inherit = "crm.team"

    incluir_propuesta_tecnica = fields.Boolean(string="Incluir propuesta técnica")
    
    company_source = fields.Selection(
        [('html', 'HTML en Odoo'), ('pdf', 'PDF subido')],
        string="Fuente Info. Empresa",
        default='html',
        required=True
    )
    
    company_info_template = fields.Html(string="Información de la empresa (HTML)")
    company_info_pdf = fields.Binary(string="Información de la empresa (PDF)")
    company_info_pdf_filename = fields.Char(string="Nombre del PDF (empresa)")
    
    service_source = fields.Selection(
        [('html', 'HTML en Odoo'), ('pdf', 'PDF subido')],
        string = "Fuente Info. Servicio",
        default = 'html',
        required=True
    )
    
    service_info_template = fields.Html(string="Información del servicio (HTML)")
    service_info_pdf = fields.Binary(string="Información del servicio (PDF)")
    service_info_pdf_filename = fields.Char(string="Nombre del PDF (servicio)")
    
    use_base_pdf = fields.Boolean("Anteponer PDF base")
    base_pdf = fields.Binary("Plantilla base (PDF)")
    base_pdf_filename = fields.Char("Nombre de archivo PDF")
    
    @api.onchange('company_source')
    def _onchange_company_source(self):
        if self.company_source == 'html':
            self.company_info_pdf = False
            self.company_info_pdf_filename = False
        elif self.company_source == 'pdf':
            self.company_info_template = False

    @api.onchange('service_source')
    def _onchange_service_source(self):
        if self.service_source == 'html':
            self.service_info_pdf = False
            self.service_info_pdf_filename = False
        elif self.service_source == 'pdf':
            self.service_info_template = False
            
    @api.constrains(
        'incluir_propuesta_tecnica',
        'company_source', 'company_info_template', 'company_info_pdf',
        'service_source', 'service_info_template', 'service_info_pdf'
    )
    def _check_team_proposal_sources(self):
        for team in self:
            if not team.incluir_propuesta_tecnica:
                continue

            if team.company_source == 'html' and not (team.company_info_template or '').strip():
                raise ValidationError(_("Debe completar la 'Información de la empresa (HTML)' o cambiar la fuente a PDF."))
            if team.company_source == 'pdf' and not team.company_info_pdf:
                raise ValidationError(_("Debe adjuntar el PDF de 'Información de la empresa'."))

            if team.service_source == 'html' and not (team.service_info_template or '').strip():
                raise ValidationError(_("Debe completar la 'Información del servicio (HTML)' o cambiar la fuente a PDF."))
            if team.service_source == 'pdf' and not team.service_info_pdf:
                raise ValidationError(_("Debe adjuntar el PDF de 'Información del servicio'."))