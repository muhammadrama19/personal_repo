from odoo import models, fields, api

class RamaRoomUser(models.Model):
    _inherit = 'res.users'
    _description = 'Extended User Model for Room Management'

    is_room_manager = fields.Boolean(string='Is Room Manager', default=False)
    room_department = fields.Char(string='Room Department')
    room_notes = fields.Text(string='Room Management Notes')
