from odoo import _, api, fields, models

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee Inherit for Transportation Management'
    is_driver = fields.Boolean(string='Is Driver', default=False)


