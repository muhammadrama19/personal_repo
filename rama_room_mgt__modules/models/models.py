# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rama_room_mgt__modules(models.Model):
#     _name = 'rama_room_mgt__modules.rama_room_mgt__modules'
#     _description = 'rama_room_mgt__modules.rama_room_mgt__modules'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

