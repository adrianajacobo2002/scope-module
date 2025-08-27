from odoo import models, fields


class SaleModuleScope(models.Model):
    _name = "sale.module.scope"
    _description = "Alcance técnico por producto/servicio"
    _order = "name"

    name = fields.Char(string="Nombre del alcance", required=True)
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Producto (plantilla)",
        required=True,
        domain=[("sale_ok", "=", True)],
    )
    team_ids = fields.Many2many(
        "crm.team",
        "sale_scope_team_rel",
        "scope_id",
        "team_id",
        string="Equipos de venta",
    )
    description_html = fields.Html(string="Alcance (HTML)")
    
    icon_image = fields.Image(
        string="Ícono del alcance", max_width=64, max_height=64,
        help="icono alcance pdf"
    )
    active = fields.Boolean(default=True)

