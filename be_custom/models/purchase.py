from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        if self.partner_id:
            lost_products = self.env['product.template'].search(
                [('vendor_id', '=', self.partner_id.id), ('is_lost_sale', '=', True)]).ids
            self.possible_lost_sales = [(4, product) for product in lost_products]
        return res

    possible_lost_sales = fields.Many2many('product.template', 'po_lost_prod_tmp_rel',
                                           'po_id', 'prod_id', string="Lost Sales")

    @api.multi
    def _create_po_lines(self, product_templates):
        po_lines = []
        for product in product_templates:
            vals = (0, 0, {
                        'name': product.name,
                        'product_qty': 1,
                        'product_id': product.product_variant_id.id,
                        'product_uom': product.uom_po_id.id,
                        'price_unit': product.standard_price,
                        'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    })
            po_lines.append(vals)
        return po_lines

    @api.multi
    def action_set_lost_products(self):
        if self.possible_lost_sales:
            po_lines = self._create_po_lines(self.possible_lost_sales)
            if po_lines:
                self.write({'order_line': po_lines})

    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for _ in self:
            buy_lost_sale = self.possible_lost_sales & self.order_line.mapped('product_id.product_tmpl_id')
            buy_lost_sale.write({'is_lost_sale':False, 'available_in_pos':True})
        return res


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