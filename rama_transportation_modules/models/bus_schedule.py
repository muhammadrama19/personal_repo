from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BusSchedule(models.Model):
    _name='bus.schedule'
    _description='Bus Schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',required=True, copy=False, default='New', readonly=True, tracking=True)
    schedule = fields.Datetime(string='Schedule', tracking=True)
    payment_type = fields.Selection(
        [
            ('cash', 'Cash'),
            ('transfer', 'Transfer')
        ],string='Payment', tracking=True
    )
    departure = fields.Datetime(string='Departure', tracking=True)
    arrival = fields.Datetime(string='Arrival', tracking=True)
    bus_id = fields.Many2one('res.bus', string='Bus', tracking=True)
    state= fields.Selection(
        [
            ('draft', 'Draft'),
            ('submit', 'Submitted'),
            ('run', 'On Going'),
            ('done', 'Done'),
        ], default='draft', tracking=True
    )
    
    @api.constrains('departure', 'arrival')
    def _check_departure_arrival(self):
        for record in self:
            if record.departure and record.arrival and record.departure > record.arrival:
                raise ValidationError('Departure time cannot be after arrival time.')
    
    @api.constrains('passenger_ids', 'capacity')
    def _check_passenger_capacity(self):
        for record in self:
            if record.capacity and len(record.passenger_ids) > record.capacity:
                raise ValidationError(f"The number of passengers ({len(record.passenger_ids)}) cannot exceed the bus capacity ({record.capacity}).")
    

    def action_submit(self):
        self.state = 'submit'
    
    def action_run(self):
        self.state = 'run'
    
    def action_done(self):
        self.state = 'done'

    bus_route_id = fields.Many2one('bus.route', string='Bus Route', tracking=True)
    baggage_line_ids = fields.One2many('baggage.baggage', 'bus_schedule_id', string='Baggage', tracking=True)
    passenger_ids = fields.Many2many('res.passenger', string='Passengers', tracking=True)
    capacity = fields.Integer(string='Capacity', store=False, related='bus_id.capacity')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('bus.schedule.seq') or '/'
        return super().create(vals_list)
    
        
