from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def create_mo(self):
        self.ensure_one()
        Procurement = self.env['procurement.order']
        MakeProcurement = self.env['make.procurement']
        MrpProductProduce = self.env['mrp.product.produce']
        make_procurement_fields = MakeProcurement.fields_get()
        mrp_product_produce = MrpProductProduce.fields_get()
        manufacture_route = self.env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)

        for product in self:
            product_vals = MakeProcurement.with_context(
                active_id=product.product_variant_id.id,
                active_model='product.product').default_get(make_procurement_fields)
            if manufacture_route:
                product_vals.update({'route_ids': [(6, 0, [manufacture_route.id])]})
            make_procure = MakeProcurement.create(product_vals)
            procure_res = make_procure.make_procurement()
            procurement_id = procure_res['res_id']

            if procurement_id:
                procurement_order = Procurement.browse(procurement_id)
                procurement_order.check()
                print procurement_id
                procurement_order.production_id.action_assign()
                product_produce = MrpProductProduce.with_context(active_id=procurement_order.production_id.id)
                product_produce_vals = product_produce.default_get(mrp_product_produce)
                product_produce = MrpProductProduce.create(product_produce_vals)
                product_produce.do_produce()
                procurement_order.production_id.post_inventory()
                procurement_order.production_id.button_mark_done()
            print 'done'
            return procurement_order.production_id
