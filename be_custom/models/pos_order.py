from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _default_session(self):
        return self.env['pos.session'].search([('state', '=', 'opened'), ('config_id.is_dummy', '=', True)], limit=1)

    session_id = fields.Many2one(default=_default_session)
    is_special_order = fields.Boolean(string='Is a Special Order?')
    vehicle_id = fields.Many2one('vehicle.vehicle', string="Customer Vehicle")


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    type = fields.Selection(related='product_id.type', string='Product Type', readonly=True)
    product_received = fields.Boolean(string="Product Received?")
