from odoo import _, api, fields, models


class BuildingFloor(models.Model):
    _name = 'rama.building.floor' 
    _description = 'Building Floor'

    sequence = fields.Integer(
        string='Sequence',
        help='Sequence of the floor in the building',
        required=True,
        default=1,
    )
    name = fields.Char(
        string='Floor Name',
        help='Name of the floor',
        required=True,
    )
    room_ids = fields.One2many(
        'rama.room',
        'floor_id',
        string='Rooms',
        help='Rooms located on this floor'
    )