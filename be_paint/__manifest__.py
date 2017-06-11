{
    'name': "BE Paint",
    'description':""" Paint customizations """,

    'summary': """
        This module is used to customize the Paint""",

    'version': '10.0.1.0.0',
    'category': '',
    'author': 'BusinessERPWeb <businesserpweb@gmail.com>',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'mrp',
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/paint_file_data.xml",
        "views/paint_product_view.xml",
    ],
    'demo': [],
    'qweb': [],
}
