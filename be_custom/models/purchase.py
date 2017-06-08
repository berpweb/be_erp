from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(PurchaseOrderLine, self).onchange_product_id()
        lines = self.search([('product_id', '=', self.product_id.id),('state', 'in', ['confirmed', 'done'])]).sorted(
            key=lambda l: l.order_id.date_order, reverse=True)
        self.last_purchase_date = lines[:1].order_id.date_order
        self.last_purchase_price = lines[:1].price_unit
        self.last_purchase_product_qty = lines[:1].product_qty
        self.last_purchase_product_uom = lines[:1].product_uom
        self.last_purchase_qty_available = self.product_id.qty_available
        self.last_purchase_product_uom_qty_available = self.product_id.uom_id
        return res

    last_purchase_price = fields.Float(string='Last Purchase Price')
    last_purchase_date = fields.Date(string='Last Purchase Date')
    last_purchase_product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    last_purchase_product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
    last_purchase_qty_available = fields.Float(string='Qty On Hand')
    last_purchase_product_uom_qty_available = fields.Many2one('product.uom', string='Product Unit of Measure')