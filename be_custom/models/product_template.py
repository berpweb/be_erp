from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    cross_ref_product_ids = fields.Many2many('product.template', 'product_cross_ref_rel', 'src_id', 'dest_id',
                                   string='Cross Reference Products', help='Suggest alternatives to your customers.')
    is_lost_sale = fields.Boolean(string="Is Lost Sale?")
    vendor_id = fields.Many2one('res.partner', string="Vendor")

    @api.onchange('vendor_id')
    def onchange_vendor_id(self):
        if self.vendor_id:
            self.seller_ids = False
            self.seller_ids = [(0, 0, {'product_tmpl_id': self.id, 'name': self.vendor_id.id})]

    @api.model
    def _get_buy_route(self):
        res = super(ProductTemplate, self)._get_buy_route()
        mto_route = self.env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
        if mto_route:
            res.extend(mto_route.ids)
        return res
