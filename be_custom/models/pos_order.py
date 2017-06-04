from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _default_session(self):
        return self.env['pos.session'].search([('state', '=', 'opened'), ('config_id.is_dummy', '=', True)], limit=1)

    session_id = fields.Many2one(default=_default_session)
    is_special_order = fields.Boolean(string='Is a Special Order?')