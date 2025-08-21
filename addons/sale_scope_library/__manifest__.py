{
    "name": "Sales Scope Library",
    "version": "17.0.1.0.0",
    "summary": "Catálogo de alcances por producto/servicio",
    "category": "",
    "author": "Adriana Jacobo",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "sales_team",
        "product",
        "web"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_module_scope_views.xml",
        "views/sale_module_scope_readonly_ro.xml",
        "views/crm_team_unlock_manager.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
}