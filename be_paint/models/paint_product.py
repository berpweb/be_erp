from odoo import fields, models


class PaintProduct(models.Model):
    _name = "paint.product"

    name = fields.Char("Date")
    data_file = fields.Binary('Paint File', attachment=True, required=True)
    filename = fields.Char()
