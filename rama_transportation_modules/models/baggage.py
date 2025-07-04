from odoo import _, api, fields, models

#class baggage

class Baggage(models.Model):
    _name = 'baggage.baggage'
    _description = 'Baggage of Passenger'

    name = fields.Char(string='Name')
    weight = fields.Float(string='Weight (Kg)')
    bus_schedule_id = fields.Many2one('bus.schedule', string='Bus Schedule')