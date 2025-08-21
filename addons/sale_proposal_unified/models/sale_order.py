from odoo import models, fields, api, _
from base64 import b64encode, b64decode
from odoo.tools import pdf as pdf_utils
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    allowed_product_ids = fields.Many2many(
        "product.product",
        string="Productos permitidos (derivados de scopes)",
        compute="_compute_allowed_products",
        compute_sudo = True,
        help="Se calcula desde sale.module.scope activo para el equipo seleccionado.",
    )

    @api.depends("team_id")
    def _compute_allowed_products(self):
        Scope = self.env["sale.module.scope"].sudo()
        for order in self:
            if not order.team_id:
                order.allowed_product_ids = [(5, 0, 0)]
                continue
            scopes = Scope.search(
                [
                    ("active", "=", True),
                    ("team_ids", "in", order.team_id.id),
                    ("product_tmpl_id", "!=", False),
                ]
            )

            variants = scopes.mapped("product_tmpl_id.product_variant_id")
            order.allowed_product_ids = [(6, 0, variants.ids)]

    @api.onchange("team_id")
    def _onchange_team_clear_incompatible_lines(self):
        self.ensure_one()
        if not self.team_id:
            return
        self._compute_allowed_products()
        bad_lines = self.order_line.filtered(
            lambda l: l.product_id
            and l.product_id.id not in self.allowed_product_ids.ids
        )
        if bad_lines:
            names = ", ".join(bad_lines.mapped("product_id.display_name"))
            for l in bad_lines:
                l.product_id = False
            return {
                'warning': {
                    'title': _('Productos no permitidos'),
                    'message': _("Se limpiaron líneas incompatibles con el equipo '%s': %s")
                               % (self.team_id.name, names)
                }
            }
        
    @api.constrains('team_id', 'order_line')
    def _check_lines_match_team(self):
        for order in self:
            if not order.team_id:
                continue
            order._compute_allowed_products()
            bad = order.order_line.filtered(
                lambda l: l.product_id and l.product_id not in order.allowed_product_ids
            )
            if bad:
                names = ', '.join(bad.mapped('product_id.display_name'))
                raise UserError(_("Los siguientes productos no pertenecen al equipo '%s': %s") %
                                (order.team_id.name, names)) 
            

    def _render_proposal_pdf(self):
        self.ensure_one()

        report_service = self.env["ir.actions.report"].sudo()
        template_name = "sale_proposal_unified.report_sale_proposal_unified_document"

        pdf_main, _ = (
            self.env["ir.actions.report"]
            .sudo()
            ._render_qweb_pdf(
                "sale_proposal_unified.report_sale_proposal_unified_document",
                [self.id],
            )
        )

        team = self.team_id
        parts = []
        
        if getattr(team, "use_base_pdf", False) and team.base_pdf:
            parts.append(b64decode(team.base_pdf))
        
        if team.company_source == 'pdf' and team.company_info_pdf:
            parts.append(b64decode(team.company_info_pdf))
            
        if team.service_source == 'pdf' and team.service_info_pdf:
            parts.append(b64decode(team.service_info_pdf))
            
        parts.append(pdf_main)
        
        merged = pdf_utils.merge_pdf(parts)
        return merged

    def action_quotation_send(self):
        action = super().action_quotation_send()
        self.ensure_one()

        if self.team_id and self.team_id.incluir_propuesta_tecnica:
            template = self.env.ref(
                "sale_proposal_unified.mail_template_sale_proposal_unified",
                raise_if_not_found=False,
            )
            ctx = dict(action.get("context", {}))
            if template:
                ctx.update(
                    {
                        "default_use_template": True,
                        "default_template_id": template.id,
                        "custom_layout": "mail.mail_notification_light",
                    }
                )

            pdf_bytes = self._render_proposal_pdf()
            if pdf_bytes:
                filename = f"Propuesta_{self.name.replace('/', '_')}.pdf"
                Attachment = self.env["ir.attachment"].sudo()
                existing = Attachment.search(
                    [
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", self.id),
                        ("name", "=", filename),
                    ],
                    limit=1,
                )
                attach_id = (
                    existing.id
                    or Attachment.create(
                        {
                            "name": filename,
                            "type": "binary",
                            "datas": b64encode(pdf_bytes),
                            "res_model": "sale.order",
                            "res_id": self.id,
                            "mimetype": "application/pdf",
                        }
                    ).id
                )

                ctx["default_attachment_ids"] = ctx.get(
                    "default_attachment_ids", []
                ) + [(4, attach_id)]

            action["context"] = ctx

        return action

    def action_print_proposal_merged(self):
        self.ensure_one()
        pdf_bytes = self._render_proposal_pdf()
        if not pdf_bytes:
            return {"type": "ir.actions.act_window_close"}
        filename = f"Propuesta_{self.name.replace('/', '_')}.pdf"
        attach = (
            self.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "name": filename,
                    "type": "binary",
                    "datas": b64encode(pdf_bytes),
                    "res_model": "sale.order",
                    "res_id": self.id,
                    "mimetype": "application/pdf",
                }
            )
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attach.id}?download=true",
            "target": "self",
        }
