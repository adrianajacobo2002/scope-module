from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    tmg_report_bg_mode = fields.Selection([
        ('none', 'Sin fondo'),
        ('color', 'Color sólido'),
        ('image_cover', 'Imagen (cubrir)'),
        ('image_contain', 'Imagen (contener)'),
        ('watermark', 'Marca de agua'),
    ], default='none', string="Modo de fondo para reportes")

    tmg_report_bg_color = fields.Char(
        default='#FFFFFF', string="Color de fondo"
    )
    tmg_report_bg_opacity = fields.Float(
        default=0.08, string="Opacidad (0–1)"
    )
    tmg_report_bg_image = fields.Binary(
        string="Imagen de fondo", attachment=True
    )
