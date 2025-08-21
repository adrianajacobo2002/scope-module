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
        "views/crm_team_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_team_visibility.xml",
        "report/sale_proposal_report_templates.xml",
        "report/sale_proposal_report.xml",
        "data/mail_template_data.xml"
    ],
    "installable": True,
    "application": True,
}