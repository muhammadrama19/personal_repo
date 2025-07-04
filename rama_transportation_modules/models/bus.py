from odoo import models, fields, api

class Bus(models.Model):
    _name = 'res.bus'
    _description = 'Bus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _constraint = [
        ('code_unique', 'UNIQUE(code)', 'The bus code must be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)
    capacity = fields.Integer(string='Capacity', tracking=True)
    image = fields.Binary(string='Image', tracking=True)
    
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('ready', 'Ready'),
            ('maintenance', 'Maintenance'),
            ('deprecated', 'Deprecated')
        ],
        readonly=False,
        tracking=True
    )
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.code} - {record.name}" if record.code else record.name
            result.append((record.id, name))
        return result
