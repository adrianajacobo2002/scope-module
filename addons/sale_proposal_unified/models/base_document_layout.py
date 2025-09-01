from odoo import models, fields

class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    tmg_report_bg_mode = fields.Selection(
        related='company_id.tmg_report_bg_mode', readonly=False
    )
    tmg_report_bg_color = fields.Char(
        related='company_id.tmg_report_bg_color', readonly=False
    )
    tmg_report_bg_opacity = fields.Float(
        related='company_id.tmg_report_bg_opacity', readonly=False
    )
    tmg_report_bg_image = fields.Binary(
        related='company_id.tmg_report_bg_image', readonly=False
    )
