from odoo import api, fields, models


class ProductTemplatePO(models.TransientModel):
    _name = 'product.template.po'
    _description = 'Product template Purchase order'

    product_ids = fields.Many2many('product.template', 'product_temp_po_rel',
                                   'temp_po_id', 'temp_id', string="Products")
    partner_id = fields.Many2one('res.partner', string="Vendor")

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplatePO, self).default_get(fields)
        context = dict(self._context or {})
        active_ids = context.get('active_ids')
        active_model = context.get('active_model')
        products = self.env[active_model].browse(active_ids)
        if products:
            seller_ids = products.mapped('seller_ids.name').ids
            if context.get('set_product_ids', False):
                res['product_ids'] = [(4, product.id) for product in products]
            res['partner_id'] = seller_ids and seller_ids[0] or []
        return res

    @api.multi
    def create_po(self):
        self.ensure_one()
        context = dict(self.env.context or {})
        Procurement = self.env['procurement.order']
        MakeProcurement = self.env['make.procurement']
        make_procurement_fields = MakeProcurement.fields_get()
        procurement_list = []
        purchase_ids = []

        for product in self.product_ids:
            product_vals = MakeProcurement.with_context(active_id=product.id, active_model='product.template').\
                default_get(make_procurement_fields)
            make_procure = MakeProcurement.create(product_vals)
            procure_res = make_procure.make_procurement()
            procurement_id = procure_res['res_id']
            procurement_list.append(procurement_id)

        if procurement_list:
            Procurement.browse(procurement_list).check()
            purchase_ids = Procurement.browse(procurement_list).mapped('purchase_id').ids

        if purchase_ids:
            return {
                'name': 'Purchase Order',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'domain': [('id', 'in', purchase_ids)],
                'res_model': 'purchase.order',
                'target': 'current',
                'context': context,
            }
