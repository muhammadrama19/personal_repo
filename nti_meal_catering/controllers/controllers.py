# -*- coding: utf-8 -*-
# from odoo import http


# class NtiMealCatering(http.Controller):
#     @http.route('/nti_meal_catering/nti_meal_catering', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nti_meal_catering/nti_meal_catering/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nti_meal_catering.listing', {
#             'root': '/nti_meal_catering/nti_meal_catering',
#             'objects': http.request.env['nti_meal_catering.nti_meal_catering'].search([]),
#         })

#     @http.route('/nti_meal_catering/nti_meal_catering/objects/<model("nti_meal_catering.nti_meal_catering"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nti_meal_catering.object', {
#             'object': obj
#         })

