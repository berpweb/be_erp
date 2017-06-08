{
    'name': "BE Custom Install",
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
        'pos_remove_pos_category',
        'web_debranding',
        'theme_kit',
        'pos_debranding',
        'pos_debt_notebook',
        'purchase_allowed_product',
        'web_sheet_full_width',
        'web_searchbar_full_width',
        'web_dialog_size',
        'pos_sale_order_clone',
        'vehicle_vehicle',
    ],
    'data': [],
    'demo': [],
    'qweb': [],
}
