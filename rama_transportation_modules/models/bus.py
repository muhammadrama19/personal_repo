from odoo import models, fields, api

class Bus(models.Model):
    _name = 'res.bus'
    _description = 'Bus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name_field'  
    _constraint = [
        ('code_unique', 'UNIQUE(code)', 'The bus code must be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)
    capacity = fields.Integer(string='Capacity', tracking=True)
    image = fields.Binary(string='Image', tracking=True)
 
    display_name_field = fields.Char(string='Display Name', compute='_compute_display_name_field', store=True)
    
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

    @api.depends('code', 'name')
    def _compute_display_name_field(self):
        for record in self:
            if record.code and record.name:
                record.display_name_field = f"[{record.code}] - {record.name}"
            elif record.code:
                record.display_name_field = f"[{record.code}]"
            elif record.name:
                record.display_name_field = record.name
            else:
                if not record._origin.id:
                    record.display_name_field = "New Bus"
                else:
                    record.display_name_field = f"Bus #{record.id}"