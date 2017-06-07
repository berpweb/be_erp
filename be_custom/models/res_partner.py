from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many('vehicle.vehicle', 'partner_id', string="Vehicles")

    @api.multi
    def open_supplied_products(self):
        self.ensure_one()
        products = self.env['product.supplierinfo'].search(
                            [('name', '=', self.id)]).mapped('product_tmpl_id')
        action = self.env.ref('stock.product_template_action_product').read()[0]
        action['domain'] = [('id', 'in', products.ids)]
        action['context'] = {}
        return action


class VehicleVehicle(models.Model):
    _inherit = 'vehicle.vehicle'

    partner_id = fields.Many2one('res.partner')
