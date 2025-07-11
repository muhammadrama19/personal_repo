from odoo import _, api, fields, models

class Room(models.Model):
    _name = 'rama.room'
    _description = 'Room Management'

    name = fields.Char(string='Room Name', required=True)
    building_id = fields.Many2one(
        'rama.building',
        string='Building',
        help='Building where the room is located',
        required=True,
    )
    capacity = fields.Integer(
        string='Capacity',
        help='Maximum number of people that can occupy the room',
        default=1,
        required=True,
    )   
    room_type_id = fields.Many2one(
        'rama.room.type',
        string='Room Type',
        help='Type of the room (e.g., conference, office, etc.)',
        required=True,
    )
    status = fields.Selection(
        [
            ('available', 'Available'),
            ('maintenance', 'Under Maintenance'),
            ('occupied', 'Occupied')
        ],
        string='Status',
        default='available',
        required=True
    )
    product_manager_id = fields.Many2one(
        'res.users',
        string='Product Manager',
        help='User responsible for managing this room',
    )
    amenities_ids = fields.Many2many(
        'rama.room.amenities',
        string='Amenities',
        help='Amenities available in this room',
    )
    
    akses_type = fields.Selection([
        ('private', 'Private'),
        ('public', 'Public')
    ], string='Access Type',
    default='public',
    required=True,
    help='Defines the access type of the room, whether it is private or public')
    
    
    available_users_ids = fields.Many2many(
        'res.users',
        string='Available Users',
        help='Users who can access this room')