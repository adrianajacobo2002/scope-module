from odoo import models, fields


class CrmTeam(models.Model):
    _inherit = "crm.team"

    incluir_propuesta_tecnica = fields.Boolean(string="Incluir propuesta técnica")
    company_info_template = fields.Html(string="Información de la empresa (HTML)")
    service_info_template = fields.Html(string="Información del servicio (HTML)")
    
    
    use_base_pdf = fields.Boolean("Anteponer PDF base")
    base_pdf = fields.Binary("Plantilla base (PDF)")
    base_pdf_filename = fields.Char("Nombre de archivo PDF")
    
    