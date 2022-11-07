# -*- coding: utf-8 -*-
from odoo import http

# class /data/cnwCabang/cnwPi(http.Controller):
#     @http.route('//data/cnw_cabang/cnw_pi//data/cnw_cabang/cnw_pi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//data/cnw_cabang/cnw_pi//data/cnw_cabang/cnw_pi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/data/cnw_cabang/cnw_pi.listing', {
#             'root': '//data/cnw_cabang/cnw_pi//data/cnw_cabang/cnw_pi',
#             'objects': http.request.env['/data/cnw_cabang/cnw_pi./data/cnw_cabang/cnw_pi'].search([]),
#         })

#     @http.route('//data/cnw_cabang/cnw_pi//data/cnw_cabang/cnw_pi/objects/<model("/data/cnw_cabang/cnw_pi./data/cnw_cabang/cnw_pi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/data/cnw_cabang/cnw_pi.object', {
#             'object': obj
#         })