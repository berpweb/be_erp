{
    'name': "BE Custom",
    'description':""" BE customizations """,

    'summary': """
        This module is used to customize the BE""",

    'version': '10.0.1.0.0',
    'category': '',
    'author': 'BusinessERPWeb <businesserpweb@gmail.com>',
    'application': True,
    'installable': True,
    'depends': [
        'point_of_sale',
        'sales_team',
        'product',
        'vehicle_vehicle',
    ],
    'data': [
        'views/pos_config_view.xml',
        'views/pos_estimate_order_view.xml',
        'views/pos_special_order_view.xml',
        'views/sale_view.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
    ],
    'demo': [],
    'qweb': [],
}
