from odoo import _, api, fields, models

class MealSchedule(models.Model):
    # Metadata
    _name = 'meal.schedule'
    _description = 'Meal Schedule that contain in a meal order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # fields sesuai requirement
    days = fields.Selection([
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    ], string='Days', required=True, help='Day of the week for the meal schedule')
    
    date = fields.Date('Date', required=True, help='Date of the meal schedule')
    time_from = fields.Float('Time From', required=True, help='Start time of the meal schedule', compute= '_change_based_on_time')
    time_to = fields.Float('Time To', required=True, help='End time of the meal schedule', compute ='_change_based_on_time')
    
    user_quantity = fields.Integer('User Quantity', required=True, 
                                  help='Quantity of meal for each user')
    adjustment_meal_quantity = fields.Integer('Adjustment Meal Quantity', required=True, 
                                            help='Adjustment quantity of meal')
    meal_quantity = fields.Integer('Meal Quantity', compute='_compute_meal_quantity', store=True, 
                                  help='Total quantity of meal (user_quantity + adjustment_meal_quantity)')
    
    meal_time = fields.Selection([
        ('morning', 'Morning'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ], string='Meal Time', required=True, help='Time of the meal')
    
    status = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='Status', required=True, help='Status of the meal schedule')
    
    # relasi ke meal.order
    meal_order_id = fields.Many2one('meal.order', string='Meal Order', required=True, 
                                   help='Meal Order for the meal schedule')
    
    # relasi ke meal.schedule.line
    meal_schedule_line_ids = fields.One2many('meal.schedule.line', 'schedule_id', 
                                           string='Meal Schedule Lines', 
                                           help='Meal Schedule Lines for the meal schedule')
    
    # relasi ke purchase order untuk tracking expense
    purchase_ids = fields.One2many('purchase.order', 'meal_schedule_id', 
                                  string='Purchase Orders', 
                                  help='Purchase Orders related to the meal schedule')
    
    @api.depends('user_quantity', 'adjustment_meal_quantity')
    def _compute_meal_quantity(self):
        # method untuk menghitung total meal quantity
        for record in self:
            record.meal_quantity = record.user_quantity + record.adjustment_meal_quantity

    @api.onchange('meal_time')
    def _change_based_on_time(self):
        for record in self:
            if record.meal_time == 'morning':
                record.time_from = 7.25 
                record.time_to = 9.00
            elif record.meal_time == 'lunch':
                record.time_from = 12.25
                record.time_to = 13.50
            else:
                record.time_from = 17.50
                record.time_to = 19.00
    
    
    @api.onchange('date')
    def _onchange_date(self):
        # method untuk auto set days berdasarkan date
        if self.date:
            # konversi weekday python (0=senin) ke format requirement (2=senin)  
            weekday = self.date.weekday()
            day_mapping = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '1'}
            self.days = day_mapping.get(weekday, '2')
    
    # smart button untuk melihat purchase orders terkait pada meal schedule
    def action_view_schedule_purchase_orders(self):
        """Smart button to view purchase orders related to this meal schedule"""
        purchase_orders = self.env['purchase.order'].search([('meal_schedule_id', '=', self.id)])
        
        
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Orders'),
            'res_model': 'purchase.order',
            'target': 'current',
            'context': {'default_meal_schedule_id': self.id},
        }
        
        if not purchase_orders:
            # fallback
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', '=', False)],  # Empty domain to show no records
            })
        elif len(purchase_orders) == 1:
          
            action.update({
                'view_mode': 'form',
                'res_id': purchase_orders.id,
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', purchase_orders.ids)],
            })
        
        return action
