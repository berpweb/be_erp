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
        'stock',
        'sales_team',
        'product',
        'account',
        'vehicle_vehicle',
        'purchase_allowed_product',
    ],
    'data': [
        'views/pos_config_view.xml',
        'views/pos_estimate_order_view.xml',
        'views/pos_special_order_view.xml',
        'views/menu_view.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
    ],
    'demo': [],
    'qweb': [],
}
