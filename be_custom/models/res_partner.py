from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many('vehicle.vehicle', 'partner_id', string="Vehicles")


class VehicleVehicle(models.Model):
    _inherit = 'vehicle.vehicle'

    partner_id = fields.Many2one('res.partner')
