{
    'name': "Vehicle",
    'description':""" Vehicle customizations """,

    'summary': """
        This module is used to customize the Vehicles""",

    'version': '10.0.1.0.0',
    'category': '',
    'author': 'BusinessERPWeb <businesserpweb@gmail.com>',
    'application': True,
    'installable': True,
    'depends': [
        'base',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/vehicle_vehicle_view.xml",
    ],
    'demo': [],
    'qweb': [],
}
