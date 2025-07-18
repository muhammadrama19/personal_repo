from odoo import models, fields, api

class Passenger(models.Model):
    _name = 'res.passenger'
    _description ='Passenger'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    weight = fields.Float(string='Weight (Kg)', tracking=True)
    height = fields.Float(string='Height (Cm)', tracking=True)
    born_date = fields.Date(string='Born Date', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)
    
    @api.depends('born_date')
    def _compute_age(self):
        for record in self:
            if record.born_date:
                today = fields.Date.today()
                born_date = fields.Date.from_string(record.born_date)
                base_age = today.year - born_date.year
                has_birthday_passed = (today.month, today.day) >= (born_date.month, born_date.day)
                if has_birthday_passed:
                    record.age = base_age
                else:
                    record.age = base_age - 1
            else:
                record.age = 0
