from odoo import _, api, fields, models


class RoomAmenities(models.Model):
    _name = 'rama.room.amenities'
    _description = 'Room Amenities'

    name = fields.Char(string='Amenities Name', required=True)
    responsible_id = fields.Many2one(
        'res.users', string='Product Manager',
        help='The user responsible for managing this room amenity'
    )
    notes = fields.Text(string='Notes', help='Additional notes about the room amenities')
