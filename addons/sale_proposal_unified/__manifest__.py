{
    "name": "Unified Sales Tech Proposal",
    "version": "17.0.1.0.0",
    "summary": "PDF unificado (empresa, servicio, alcances, economía) + email",
    "category": "",
    "author": "Adriana Jacobo",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "sales_team",
        "mail",
        "web",
        "sale_scope_library"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/report_paperformat.xml",
        "views/crm_team_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_team_visibility.xml",
        "views/report_saleorder_bg.xml",
        "report/sale_proposal_report_templates.xml",
        "report/sale_proposal_report.xml",
    ],
    "installable": True,
    "application": True,
    'assets': {
        'web.report_assets_common': [
            'sale_proposal_unified/static/src/css/report_bg.css',
            'sale_proposal_unified/static/src/css/report_proposal.css',
        ],
    }
}