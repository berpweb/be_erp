from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    cross_ref_product_ids = fields.Many2many('product.template', 'product_cross_ref_rel', 'src_id', 'dest_id',
                                   string='Cross Reference Products', help='Suggest alternatives to your customers.')
