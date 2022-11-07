# -*- coding: utf-8 -*-
{
    'name': "INDOGUNA - INCOME EXPENSE PAYMENT",

    'summary': """
        INDOGUNA - INCOME EXPENSE PAYMENT """,

    'description': """
        INDOGUNA - INCOME EXPENSE PAYMENT
    """,

    'author': "Indoguna Utama,Andy Utomo",
    'website': "http://www.indoguna.id",

 
    'category': 'others',
    'version': '0.1',
    'application':True,

    # any module necessary for this one to work correctly
    'depends': ['base','cnw_numbering'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/master_views.xml',
        'views/jp_views.xml',
        'views/coa_views.xml',
        'views/inex_numbering.xml',
        'menu/menu.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}