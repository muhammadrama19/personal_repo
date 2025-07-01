from odoo import models, fields, api

class Passenger(models.Model):
    _name = 'res.passenger'
    _description ='Passenger'

    name = fields.Char(string='Name', required=True)
    weight = fields.Float(string='Weight (Kg)')
    height = fields.Float(string='Height (Cm)')
    born_date = fields.Date(string='Born Date')
