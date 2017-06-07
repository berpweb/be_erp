from odoo import fields, models


class VehicleMake(models.Model):
    _name = "vehicle.make"

    name = fields.Char(string="Make name?")


class VehicleColor(models.Model):
    _name = "vehicle.color"

    name = fields.Char(string="Color?")


class VehicleVehicle(models.Model):
    _name = "vehicle.vehicle"

    name = fields.Char(string="Plat Number?")
    vehicle_make = fields.Many2one('vehicle.make', string="Vehicle Make?")
    vehicle_model = fields.Char(string="Vehicle Model?")
    vehicle_year = fields.Char(string="Year?")
    vehicle_color = fields.Many2one('vehicle.color', string="Vehicle Color?")
    vehicle_vin_number = fields.Char(string="VIN number?")
