# -*- coding: utf-8 -*-
{
    'name': "CNW-SAP Business Partner",

    'summary': """
        CNW-SAP Business Partner """,

    'description': """
       CNW-SAP Business Partner
    """,

    'author': "Indoguna Utama, Andy Utomo",
    'website': "http://www.indoguna.id",
    'application':True,

     
    'category': 'others',
    'version': '0.1',

 
    'depends': ['base'],
 
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/pi_views.xml',
        'views/pi_jenis_views.xml',
        'views/piaju_views.xml',
        'views/hs_views.xml',
        'views/templates.xml',
        'menu/menu.xml',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
}