from odoo import api, fields, models

class RoomType(models.Model):
    _name = 'rama.room.type'
    _description = 'Room Type'

    name = fields.Char(string='Room Type Name', required=True)
    quantity = fields.Integer(string='Quantity', required=True, default=1)

    