import re
from openerp.exceptions import ValidationError
from openerp import fields, models, api
from datetime import date


class task(models.Model):
    _name = 'task.test'
    _order = 'id desc'
    _rec_name = 'user_name'

    user_name = fields.Char("User Name")
    mobile = fields.Char("Mobile Number")
    age = fields.Integer("Age")
    remarks = fields.Text()
    task_line_id = fields.One2many('task.test.line', 'task_ticket_id', 'Task Line', required=True)
    state = fields.Selection(
        [('confirmed', 'Confirmed'), ('approved', 'Approved'), ('cancelled', 'Cancelled')],
        'Status', default='confirmed', readonly=True)
    total = fields.Float(string="Total (BDT)")


# All field validation part start
    @api.constrains('mobile')
    def validate_mobile_number(self):
        if self.mobile:
            validate_mobile_num = re.match('^01[0-9]{9}$', self.mobile)
            if not validate_mobile_num:
                raise ValidationError('Mobile number must be numeric value and 11 digit long')

    # @api.multi
    # @api.constrains('mobile')
    # def _check_mobile(self):
    #     for rec in self:
    #         if rec.mobile and len(rec.mobile) != 11:
    #             raise ValidationError(_("Mobile number must be numeric value and 11 digit long"))
    #     return True

    @api.constrains('age')
    def validate_age(self):
        for record in self:
            if record.age < 18:
                raise ValidationError('Age must be 18 years or older')

# All field validation part ends

# header button's function start
    def task_cancel(self, cr, uid, ids, context=None):
        if ids is not None:
            cr.execute("update task_test set state='cancelled' where id=%s", (ids))
            cr.commit()
        return True

    def task_confirm(self, cr, uid, ids, context=None):
        if ids is not None:
            cr.execute("update task_test set state='confirmed' where id=%s", (ids))
            cr.commit()
        return True

    def task_approve(self, cr, uid, ids, context=None):
        if ids is not None:
            cr.execute("update task_test set state='approved' where id=%s", (ids))
            cr.commit()
        return True

#   header button's function ends


    @api.onchange('task_line_id')
    def onchange_total(self):
        total = 0
        for sub_total in self.task_line_id:
            total = total + sub_total.unit_price
        self.total = total


class task_line(models.Model):
    _name = 'task.test.line'
    task_ticket_id = fields.Many2one('task.test', "Task Info")
    name = fields.Many2one('task.test.entry', ondelete='cascade')
    date = fields.Date("Date", default=fields.Date.today())
    unit_price = fields.Integer("Unit Price")
    quantity = fields.Integer("Quantity", default=1)
    unit_sub_total = fields.Float("Sub Total")
    note = fields.Char("Note")


class task_entry(models.Model):
    _name = 'task.test.entry'
    _order = 'id desc'
    name = fields.Char("Task Name")
