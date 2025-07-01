from odoo import models, fields, api

class BusRoutes(models.Model):
    _name= 'bus.route'
    _description = 'Bus Route'

    name = fields.Char(string='Name')
    