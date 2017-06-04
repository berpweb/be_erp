from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_dummy = fields.Boolean(string='Is a dummy POS?')
    sequence_id = fields.Many2one('ir.sequence', readonly=False)
