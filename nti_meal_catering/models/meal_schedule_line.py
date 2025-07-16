from odoo import _, api, fields, models

class MealScheduleLine(models.Model):
    # Metadata
    _name = 'meal.schedule.line'
    _description = 'Meal Schedule Line in Meal Catering'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # menu is represented by product_id
    product_id = fields.Many2one('product.product', string='Menu', required=True, help='Menu for the meal schedule line')
    
    # : product_category_id bukan category_id
    product_category_id = fields.Many2one('product.category', string='Menu Category', 
                                        related='product_id.categ_id', store=True,
                                        help='Category of the meal menu (Lauk/Buah/Sayur)')
    
    # each meal schedule has it own bom_id which is the bill of material for the meal schedule line
    # domain dikasih : hanya tampil yang ada di bom_ids dalam product
    bom_id = fields.Many2one('mrp.bom', string='Bill of Material', required=True,
                            domain="[('product_tmpl_id', '=', product_tmpl_id)]",
                            help='Bill of Material for the meal schedule line')
    
    # hidden field untuk domain filtering
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=False)
    
    # relationship to meal.schedule because each meal schedule line is belong to a meal schedule
    schedule_id = fields.Many2one('meal.schedule', string='Meal Schedule', required=True, help='Meal Schedule for the meal schedule line')
    
    # quantity 
    quantity = fields.Float('Quantity', required=True, help='Quantity of the meal schedule line', default=1.0)
    
    # computed field to show meal order sequence and day
    schedule_display = fields.Char('Schedule', compute='_compute_schedule_display', store=True,
                                  help='Display meal order sequence and day')
    
    @api.depends('schedule_id.meal_order_id.name', 'schedule_id.days')
    def _compute_schedule_display(self):
        # method untuk menampilkan sequence meal order dan hari
        for record in self:
            if record.schedule_id and record.schedule_id.meal_order_id:
                day_name = dict(record.schedule_id._fields['days'].selection).get(record.schedule_id.days, '')
                record.schedule_display = f"{record.schedule_id.meal_order_id.name} - {day_name}"
            else:
                record.schedule_display = ""
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        # jika memang product_id terisi
        if self.product_id:
            # reset bom_id 
            self.bom_id = False
            # ambil bom pertama yang tersedia untuk product ini
            bom = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)
            ], limit=1)
            # jika emg bom ditemukan, set bom_id
            if bom:
                self.bom_id = bom.id
            
            # return domain untuk bom_id
            return {
                'domain': {
                    'bom_id': [('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)]
                }
            }
        # if no, reset lagi
        else:
            self.bom_id = False
            return {
                'domain': {
                    'bom_id': [('id', '=', False)]
                }
            }



