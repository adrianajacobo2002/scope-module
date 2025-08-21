from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_scope_html = fields.Html(
        string="Alcance personalizado",
        help="Usa esto cuando no exista un scope estándar para este producto/servicio."
    )
