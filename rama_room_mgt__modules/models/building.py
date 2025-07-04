from odoo import _, api, fields, models

class Building(models.Model):
    _name = 'rama.building'
    _description = 'Building'

    name = fields.Char(string='Building Name', required=True)
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible User',
        help='User responsible for this building',
        required=True,
    )
    number_of_floors = fields.Integer(
        string='Number of Floors',
        help='Total number of floors in the building',
        required=True,
    )
    date_of_built = fields.Date(
        string='Date of Built',
        help='Date when the building was constructed',
        required=True,
    )
    address = fields.Char(
        string='Address',
        help='Physical address of the building',
        required=True,
    )
    longitude = fields.Char(
        string='Longitude',
        help='Geographical longitude of the building location',
        required=True,
    )
    latitude = fields.Char(
        string='Latitude',
        help='Geographical latitude of the building location',
        required=True,
    )
    notes = fields.Text(
        string='Notes',
        help='Additional notes or comments about the building',
    )
