# -*- coding: utf-8 -*-
# from odoo import http


# class RamaRoomMgtModules(http.Controller):
#     @http.route('/rama_room_mgt__modules/rama_room_mgt__modules', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rama_room_mgt__modules/rama_room_mgt__modules/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rama_room_mgt__modules.listing', {
#             'root': '/rama_room_mgt__modules/rama_room_mgt__modules',
#             'objects': http.request.env['rama_room_mgt__modules.rama_room_mgt__modules'].search([]),
#         })

#     @http.route('/rama_room_mgt__modules/rama_room_mgt__modules/objects/<model("rama_room_mgt__modules.rama_room_mgt__modules"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rama_room_mgt__modules.object', {
#             'object': obj
#         })

