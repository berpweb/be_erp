import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def create_mo(self):
        self.ensure_one()
        Procurement = self.env['procurement.order']
        MakeProcurement = self.env['make.procurement']
        MrpProductProduce = self.env['mrp.product.produce']
        make_procurement_fields = MakeProcurement.fields_get()
        mrp_product_produce_fields = MrpProductProduce.fields_get()
        manufacture_route = self.env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)

        product_vals = MakeProcurement.with_context(
            active_id=self.product_variant_id.id,
            active_model='product.product').default_get(make_procurement_fields)
        if manufacture_route:
            product_vals.update({'route_ids': [(6, 0, [manufacture_route.id])]})
        make_procure = MakeProcurement.create(product_vals)
        _logger.info("Created MakeProcurement: ID - %s", make_procure.id)
        procure_res = make_procure.make_procurement()
        procurement_id = procure_res['res_id']
        _logger.info("Created Procurement: ID - %s", procurement_id)

        if procurement_id:
            procurement_order = Procurement.browse(procurement_id)
            procurement_order.check()
            production = procurement_order.production_id
            _logger.info("Created Production: ID - %s", production.id)
            production.action_assign()
            product_produce = MrpProductProduce.with_context(active_id=production.id)
            product_produce_vals = product_produce.default_get(mrp_product_produce_fields)
            product_produce = MrpProductProduce.create(product_produce_vals)
            product_produce.do_produce()
            production.post_inventory()
            production.button_mark_done()
            _logger.info("Production Completed: ID - %s", production.id)
            return production, procurement_order
        return False, False
