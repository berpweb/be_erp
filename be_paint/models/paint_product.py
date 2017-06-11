import itertools
import datetime
import logging

from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None


class PaintProduct(models.Model):
    _name = "paint.product"

    name = fields.Char("Date")
    data_file = fields.Binary('Paint File', attachment=True, required=True)
    filename = fields.Char()
    production_id = fields.Many2one('mrp.production', 'Production')
    procurement_id = fields.Many2one('procurement.order', 'Procurement')

    @api.multi
    def action_build_paint_product(self):
        _logger.info("Starting to read excel file")
        try:
            rows = self._read_xls()
            data = [list(row) for row in rows if any(row)]
            if data:
                main_product = self._prepare_paint_product(data)
                _logger.info("Prepared Main Product - %s", main_product)
                if main_product:
                    production, procurement_order = self._build_paint_product(main_product)
                    _logger.info("Got production - %s and procurement - %s", production, procurement_order)
                    self.production_id = production
                    self.procurement_id = procurement_order
        except Exception, error:
            _logger.info("Error during paint product building", exc_info=True)

    @api.multi
    def _read_xls(self):
        self.ensure_one()
        file_data = self.data_file.decode('base64')
        book = xlrd.open_workbook(file_contents=file_data)
        return self._read_xls_book(book)

    @api.model
    def _read_xls_book(self, book):
        sheet = book.sheet_by_index(0)
        # emulate Sheet.get_rows for pre-0.9.4
        for row in itertools.imap(sheet.row, range(sheet.nrows)):
            values = []
            for cell in row:
                if cell.ctype is xlrd.XL_CELL_NUMBER:
                    is_float = cell.value % 1 != 0.0
                    values.append(
                        unicode(cell.value)
                        if is_float
                        else unicode(int(cell.value))
                    )
                elif cell.ctype is xlrd.XL_CELL_DATE:
                    is_datetime = cell.value % 1 != 0.0
                    # emulate xldate_as_datetime for pre-0.9.3
                    dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(cell.value, book.datemode))
                    values.append(
                        dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        if is_datetime
                        else dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                    )
                elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
                    values.append(u'True' if cell.value else u'False')
                elif cell.ctype is xlrd.XL_CELL_ERROR:
                    raise ValueError(
                        _("Error cell found while reading XLS/XLSX file: %s") %
                        xlrd.error_text_from_code.get(
                            cell.value, "unknown error code %s" % cell.value)
                    )
                else:
                    values.append(cell.value)
            if any(x for x in values if x.strip()):
                yield values

    @api.model
    def _prepare_paint_product(self, rows):
        main_product = {}
        for row in rows[:5]:
            if row[0] == 'Chip number:':
                main_product.update({'part_number': row[1] or 000000})
            elif row[0] == 'Manufacturer:':
                main_product.update({'manufacturer': row[1] or False})
            elif row[0] == 'Color code:':
                main_product.update({'color_code': row[1] or False})
            elif row[0] == 'Color name:':
                main_product.update({'color_name': row[1] or False})
            elif row[0] == 'Quantity:':
                main_product.update({'qty': row[1] or 0})
        for row in rows[-1:]:
            if row[1] == 'Total:':
                main_product.update({'price': row[2] or 0})
        main_product.update({'bom_products': rows[6:-1]})
        return main_product

    @api.multi
    def _build_paint_product(self, main_product):
        self.ensure_one()
        ProductTemplate = self.env['product.template']
        MrpBom = self.env['mrp.bom']
        MrpBomLine = self.env['mrp.bom.line']
        bom_products = []
        product_template_fields = ProductTemplate.fields_get()
        mrp_bom_fields = MrpBom.fields_get()
        mrp_bom_line_fields = MrpBomLine.fields_get()
        if main_product:
            product = ProductTemplate.search([('default_code','=',main_product['part_number'])])
            if product:
                _logger.info("Main Product already exists. ID - %s, Name - %s", product.id, product.name)
                pass # update to existing product, instead of creating new one
            else:
                for bom in main_product['bom_products']:
                    bom_products.append(ProductTemplate.search([('default_code', '=', bom[0])]))
                _logger.info("Created BOM Products - %s", bom_products)
                template_defaults = ProductTemplate.default_get(product_template_fields)
                manufacture_route = self.env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
                template_defaults.update({
                    'default_code': main_product['part_number'],
                    'name': main_product['color_name'],
                    'type': 'product',
                    'route_ids':[(6, 0, [manufacture_route.id])],
                })
                product = ProductTemplate.create(template_defaults)
                _logger.info("Created New Product - %s", product.id)
                if bom_products and product:
                    bom_defaults = MrpBom.default_get(mrp_bom_fields)
                    bom_defaults.update({
                        'product_tmpl_id': product.id,
                        'product_qty': 1,
                    })
                    bom = MrpBom.create(bom_defaults)
                    _logger.info("Created BOM - %s for Product - %s", bom.id, product.id)
                    for bom_product in bom_products:
                        lines_default = MrpBomLine.default_get(mrp_bom_line_fields)
                        lines_default.update({
                            'product_id': bom_product.product_variant_id.id,
                            'bom_id': bom.id,
                            # 'product_qty': 1,
                        })
                        bom_line = MrpBomLine.create(lines_default)
                        _logger.info("Created BOM Line - %s for BOM - %s with Product - %s",
                                     bom_line.id, bom.id, bom_product.product_variant_id.id)
            if product:
                _logger.info("Creating MO for ID - %s, Product - %s", product.id, product.name)
                return product.create_mo()
