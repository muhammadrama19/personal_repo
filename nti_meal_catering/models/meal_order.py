from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta

class MealOrder(models.Model):
    # Metadata
    _name = 'meal.order'
    _description = 'Meal Order in Meal Catering'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # fields sesuai requirement baru
    name = fields.Char('Name', required=True, help='Name of the meal order', default='/', readonly=True)
    
    chef_id = fields.Many2one('hr.employee', string='Default Chef', required=True, 
                             help='Chef who prepares the meal')
    
    responsible_id = fields.Many2one('res.users', string='Responsible', required=True, 
                                     default=lambda self: self.env.user,
                                     help='User responsible for the meal order')
   
    # method untuk mendapatkan tanggal senin minggu depan
    def _get_next_week_monday(self):
        today = fields.Date.context_today(self)
        weekday = today.weekday()
        days_until_monday = 7 - weekday
        next_monday = today + timedelta(days=days_until_monday)
        return next_monday

    # method untuk mendapatkan tanggal jumat minggu depan  
    def _get_next_week_friday(self):
        next_monday = self._get_next_week_monday()
        next_friday = next_monday + timedelta(days=4)
        return next_friday
    
    date_from = fields.Date('Date From', required=True, 
                           help='Date from which the meal order is valid',
                           default=_get_next_week_monday)

    date_to = fields.Date('Date To', required=True, 
                         help='Date until which the meal order is valid',
                         default=_get_next_week_friday)
   
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('on_going', 'On Going'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True, 
       help='Status of the meal order', tracking=True)
    
    basic_quantity_user = fields.Integer('Basic Quantity per User', required=True, 
                                        help='Basic quantity of meal per user')
    
    budget = fields.Monetary('Budget', required=True, 
                            help='Budget for the meal order')
    
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, 
                                  help='Currency of the budget', 
                                  default=lambda self: self.env.company.currency_id)

    # relasi ke meal.schedule
    meal_schedule_ids = fields.One2many('meal.schedule', 'meal_order_id', 
                                       string='Meal Schedules', 
                                       help='Meal Schedules for the meal order')
  
    # computed fields 
    total_expense = fields.Monetary('Total Expense', compute='_compute_total_expense', 
                                   currency_field='currency_id', store=True,
                                   help='Total expense from all purchase orders')
    
    purchase_count = fields.Integer('Purchase Count', compute='_compute_purchase_count', 
                                   store=True, help='Total number of purchase orders')
    
    @api.depends('meal_schedule_ids.purchase_ids.amount_total')
    def _compute_total_expense(self):
        # method untuk menghitung total expense dari purchase order
        for record in self:
            total = 0.0
            for schedule in record.meal_schedule_ids:
                for purchase in schedule.purchase_ids:
                    total += purchase.amount_total
            record.total_expense = total
    
    @api.depends('meal_schedule_ids.purchase_ids')
    def _compute_purchase_count(self):
        # method untuk menghitung jumlah purchase order
        for record in self:
            count = 0
            for schedule in record.meal_schedule_ids:
                count += len(schedule.purchase_ids)
            record.purchase_count = count

    @api.model
    def create(self, vals):
        # method untuk auto create meal schedules senin-jumat ketika meal order dibuat
        record = super().create(vals)
        if record.date_from and record.date_to:
            record._create_meal_schedules()
        return record

    def _create_meal_schedules(self):
        # method untuk membuat meal schedule otomatis dari senin ke jumat
        current_date = self.date_from
        # loop till date_to
        while current_date <= self.date_to:
            # skip weekend (sabtu=5, minggu=6)
            if current_date.weekday() < 5:  
                # ambil day sesuai format requirement (1=minggu, 2=senin dst)
                day_mapping = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6'}  # senin=2, selasa=3, dst
                day_value = day_mapping.get(current_date.weekday(), '2')
                
                self.env['meal.schedule'].create({
                    'meal_order_id': self.id,
                    'date': current_date,
                    'days': day_value,
                    'time_from': 12.0,  
                    'time_to': 13.0,    
                    'user_quantity': self.basic_quantity_user,
                    'adjustment_meal_quantity': 0,
                    'meal_time': 'lunch',  # default lunch
                    'status': 'open',
                })
            current_date += timedelta(days=1)

    # function untuk perubahan state sesuai requirement
    def action_submit(self):
        # method untuk mengubah state menjadi 'submitted' dan generate sequence
        if self.name == '/':
            self.name = self.env['ir.sequence'].next_by_code('meal.order') or '/'
        self.write({'state': 'submitted'})

    def action_confirm(self):
        # method untuk mengubah state menjadi 'on_going' dan create purchase order
        self.write({'state': 'on_going'})
        self.create_purchase_orders()

    def action_done(self):
        # method untuk mengubah state menjadi 'done'
        self.write({'state': 'done'})

    def action_cancel(self):
        # method untuk mengubah state menjadi 'canceled'
        self.write({'state': 'canceled'})

    def action_reject(self):
        # method untuk mengubah state menjadi 'rejected'
        self.write({'state': 'rejected'})

    def action_view_purchase_orders(self):
        # method untuk menampilkan purchase orders terkait meal order
        purchase_orders = self.env['purchase.order'].search([
            ('meal_schedule_id', 'in', self.meal_schedule_ids.ids)
        ])
        
        action = {
            'name': 'Purchase Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'target': 'current',
        }
        
        if len(purchase_orders) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': purchase_orders.id,
            })
        else:
            action['domain'] = [('id', 'in', purchase_orders.ids)]
            
        return action

    def create_purchase_orders(self):
        # step 1: kumpulkan semua product
        product_requirements = self._collect_product_requirements()
        
        # step 2: grup berdasarkan schedule
        grouped_requirements = self._group_by_sched(product_requirements)
        
        # step 3: buat purchase orders (satu per schedule)
        purchase_orders = self._create_pos_from_requirements(grouped_requirements)
        
        # step 4: assign ke schedules
        self._assign_pos_to_schedules(purchase_orders)

    def _collect_product_requirements(self):
        requirements = []
        
        # loop ke semua meal schedules
        for schedule in self.meal_schedule_ids:
            # loop ke semua meal schedule lines
            for line in schedule.meal_schedule_line_ids:
                #if no bom skip
                if not line.bom_id:
                    continue
                
                # if found bom, loop ke semua bom lines
                for bom_line in line.bom_id.bom_line_ids:
                    product = bom_line.product_id
                    total_quantity = bom_line.product_qty * line.quantity * schedule.meal_quantity
                    
                    # No need to check suppliers since we use super supplier
                    requirements.append({
                        'schedule_id': schedule.id,
                        'product_id': product.id,
                        'product': product,
                        'quantity': total_quantity,
                        'uom': bom_line.product_uom_id,
                        'price_unit': product.standard_price,  # Use standard price
                    })
        
        return requirements

    def _group_by_sched(self, requirements):
        grouped = {}
        
        # restruktur data requirements - hanya berdasarkan schedule
        for req in requirements:
            schedule_id = req['schedule_id']
            product_id = req['product_id']
            
            # inisialisasi struktur data
            if schedule_id not in grouped:
                grouped[schedule_id] = {
                    'schedule': self.env['meal.schedule'].browse(schedule_id),
                    'products': {}
                }
            
            # agregasi quantity untuk product yang sama
            schedule_products = grouped[schedule_id]['products']
            if product_id in schedule_products:
                schedule_products[product_id]['quantity'] += req['quantity']
            else:
                schedule_products[product_id] = {
                    'product': req['product'],
                    'quantity': req['quantity'],
                    'uom': req['uom'],
                    'price_unit': req['price_unit'],
                }
        
        return grouped

    def _create_pos_from_requirements(self, grouped_requirements):
        purchase_orders = []
        # override supplier
        super_supplier = self.env['res.partner'].search([('name', '=', 'Mimi Borma')], limit=1)
        if not super_supplier:
            raise ValueError("Super Supplier tidak ditemukan!")

        # loop untuk membuat purchase orders dari grouped requirements
        for schedule_id, schedule_data in grouped_requirements.items():
            schedule = schedule_data['schedule']
            products = schedule_data['products']
            
            if not products:
                continue

            order_lines = [(0, 0, {
                'product_id': product_data['product'].id,
                'product_qty': product_data['quantity'],
                'product_uom': product_data['uom'].id,
                'price_unit': product_data['price_unit'],
            }) for product_data in products.values()]

            po_vals = {
                'partner_id': super_supplier.id,
                'meal_schedule_id': schedule.id,
                'order_line': order_lines
            }
            
            # generate purchase order
            try:
                po = self.env['purchase.order'].create(po_vals)
                purchase_orders.append({
                    'po': po,
                    'schedule_id': schedule.id
                })
            except Exception:
                continue  # skip jika creation gagal
        
        return purchase_orders

    def _assign_pos_to_schedules(self, purchase_orders):
        for po_data in purchase_orders:
            schedule_id = po_data['schedule_id']
            schedule = self.env['meal.schedule'].browse(schedule_id)
            schedule.write({'purchase_ids': [(6, 0, [po_data['po'].id])]})