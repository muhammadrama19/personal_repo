# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rama_transportation_modules(models.Model):
#     _name = 'rama_transportation_modules.rama_transportation_modules'
#     _description = 'rama_transportation_modules.rama_transportation_modules'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

