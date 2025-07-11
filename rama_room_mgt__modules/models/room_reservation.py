from odoo import _, api, fields, models


class RoomReservation(models.Model):
    _name = 'rama.room.reservation'
    _description = 'Room Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, copy=False, default='New', readonly=True)
    room_id = fields.Many2one('rama.room', string='Room')
    request_user_id = fields.Many2one('res.users', string='Requested By', required=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible User', related='room_id.product_manager_id', store=True)
    request_datetime = fields.Datetime('Request Date', readonly=True, default=fields.Datetime.now)
    start_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    purpose = fields.Char('Purpose')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected')
        
    ], string='State', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('room.reservation.seq') or '/'
        return super().create(vals_list)
        
    def action_submit(self):
       
        for record in self:
            if record.state != 'draft':
                raise models.ValidationError(_("Only draft reservations can be submitted."))
                
            record.write({'state': 'submit'})
            record.message_post(body=_("Reservation submitted by %s") % self.env.user.name)
        
    def action_confirm(self):
        
        for record in self:
            if record.state != 'submit':
                raise models.ValidationError(_("Only submitted reservations can be confirmed."))
                
            record.write({'state': 'confirm'})
            record.message_post(body=_("Reservation confirmed by %s") % self.env.user.name)
        
    def action_done(self):
        
        for record in self:
            if record.state != 'confirm':
                raise models.ValidationError(_("Only confirmed reservations can be marked as done."))
                
            record.write({'state': 'done'})
            record.message_post(body=_("Reservation marked as done by %s") % self.env.user.name)
        
    def action_cancel(self):
    
        for record in self:
            if self.env.user.id not in [record.request_user_id.id, record.responsible_user_id.id]:
                raise models.ValidationError(_("Only the requester or room manager can cancel this reservation."))
            
            if record.state != 'confirm':
                raise models.ValidationError(_("Only confirmed reservations can be cancelled."))
                
            record.write({'state': 'cancel'})
            record.message_post(body=_("Reservation cancelled by %s") % self.env.user.name)
        
    def action_reject(self):
        
        for record in self:
            if self.env.user.id != record.responsible_user_id.id:
                raise models.ValidationError(_("Only the room manager can reject this reservation."))
                
            if record.state != 'confirm':
                raise models.ValidationError(_("Only confirmed reservations can be rejected."))
                
            record.write({'state': 'reject'})
            record.message_post(body=_("Reservation rejected by %s") % self.env.user.name)

