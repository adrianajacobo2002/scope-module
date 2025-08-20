from odoo import models
from base64 import b64encode, b64decode
from odoo.tools import pdf as pdf_utils


class SaleOrder(models.Model):
    _inherit = "sale.order"

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
        if getattr(team, "use_base_pdf", False) and team.base_pdf:
            base_bytes = b64decode(team.base_pdf)
            pdf_main = pdf_utils.merge_pdf([base_bytes, pdf_main])

        return pdf_main

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
