# -*- coding: utf-8 -*-
# WR Ltd

{
    'name': 'Sales Discount Workflow',
    'version': '1.1',
    'author':'WR Ltd',
    'summary': 'Sales Discount Workflow',
    'description': """
Sales Discount Workflowe
======================

""",
    'website': 'https://cloud.wrltd.ca',
    'depends': ['base_setup','sale', 'sales_team'],
    'data': [
        'views/res_user_views.xml',
        'views/sale_view.xml',
    ],    
    'installable': True,
    'auto_install': False,
}
