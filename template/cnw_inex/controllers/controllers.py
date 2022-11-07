# -*- coding: utf-8 -*-
from odoo import http

# class /data/iguItDev/cnwJe(http.Controller):
#     @http.route('//data/igu_it_dev/cnw_je//data/igu_it_dev/cnw_je/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//data/igu_it_dev/cnw_je//data/igu_it_dev/cnw_je/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/data/igu_it_dev/cnw_je.listing', {
#             'root': '//data/igu_it_dev/cnw_je//data/igu_it_dev/cnw_je',
#             'objects': http.request.env['/data/igu_it_dev/cnw_je./data/igu_it_dev/cnw_je'].search([]),
#         })

#     @http.route('//data/igu_it_dev/cnw_je//data/igu_it_dev/cnw_je/objects/<model("/data/igu_it_dev/cnw_je./data/igu_it_dev/cnw_je"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/data/igu_it_dev/cnw_je.object', {
#             'object': obj
#         })