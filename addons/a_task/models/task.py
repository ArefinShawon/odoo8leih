from openerp import api
from openerp.osv import fields, osv


class task_ticket(osv.osv):
    _name = "task.test"
    _order = 'id desc'

    _columns = {
        'user_name': fields.char("User Name"),
        'remarks': fields.char("Remarks"),
        'task_line_id': fields.one2many('task.test.line', 'task_ticket_id', 'Task Line', required=True),
        'state': fields.selection(
            [('confirmed', 'Confirmed'), ('approved', 'Approved'), ('cancelled', 'Cancelled')],
            'Status', default='confirmed', readonly=True),
        'total': fields.float(string="Total"),
    }


    @api.onchange('task_line_id')
    def onchange_total(self):
        total = 0
        for sub_total in self.task_line_id:
            total = total + sub_total.subtask_amount
        self.total = total


class test_information(osv.osv):
    _name = 'task.test.line'
    _columns = {
        'name': fields.many2one("task.test.entry", ondelete='cascade'),
        'task_ticket_id': fields.many2one('task.test', "Task Info"),
        'date': fields.date("Date", default=fields.date.today()),
        'subtask_amount': fields.integer("Task-wise Amount"),
        'note': fields.char("Note"),
    }


class task_ticket_config(osv.osv):
    _name = "task.test.entry"
    _order = 'id desc'
    _columns = {
        'name': fields.char("Task Name"),
    }
