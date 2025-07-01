# -*- coding: utf-8 -*-
# from odoo import http


# class RamaTransportationModules(http.Controller):
#     @http.route('/rama_transportation_modules/rama_transportation_modules', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rama_transportation_modules/rama_transportation_modules/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rama_transportation_modules.listing', {
#             'root': '/rama_transportation_modules/rama_transportation_modules',
#             'objects': http.request.env['rama_transportation_modules.rama_transportation_modules'].search([]),
#         })

#     @http.route('/rama_transportation_modules/rama_transportation_modules/objects/<model("rama_transportation_modules.rama_transportation_modules"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rama_transportation_modules.object', {
#             'object': obj
#         })

