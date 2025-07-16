from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    # field untuk menghubungkan purchase order dengan meal schedule
    meal_schedule_id = fields.Many2one('meal.schedule', string='Meal Schedule',
                                     help='Meal Schedule that this purchase order belongs to')
