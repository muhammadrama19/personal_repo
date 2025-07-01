from odoo import models, fields, api

class BusSchedule(models.Model):
    _name='bus.schedule'
    _description='Bus Schedule'

    name = fields.Char(string='Name')
    schedule = fields.Datetime(string='Schedule')
    payment_type = fields.Selection(
        [
            ('cash', 'Cash'),
            ('transfer', 'Transfer')
        ],string='Payment'
    )
    departure = fields.Datetime(string='Departure')
    arrival = fields.Datetime(string='Arrival')







    
