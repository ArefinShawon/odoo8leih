import re
from openerp.exceptions import ValidationError

from openerp import api, _
from openerp.osv import fields, osv

# This is the main part of the customer order list with One to Many relationship:



class inventory_item(osv.osv):
    _name = "inventory.item"
    _order = 'id asc'
    _rec_name = "name"

    _columns = {

        'name': fields.char("Name",),
        'phone': fields.char("Mobile", required=True),
        'customer_name': fields.char("Customer Name", required=True),
        'age': fields.integer("Age"),
        'date': fields.date("Date", readonly=True, default=lambda self: fields.datetime.now()),
        'inventory_line_id': fields.one2many('inventory.item.line', 'inventory_item_id', required=True),
        'state': fields.selection(
            [('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'),('approved', 'approved')],
            'Status', default='confirmed', readonly=True),
        'total': fields.float(string="Total"),
    }

# This part is used for Mobile Number verification
    @api.depends('phone')
    @api.onchange('phone')
    def validate_phone(self):
        if self.phone:
            match = re.match(r'^[0][1][0-9]{9}$', self.phone)
            if match == None:
                raise ValidationError('Enter Mobile number')

# This part is used for the Age validation
    @api.constrains('age')
    def val_age(self):
        for record in self:
           if record.age <= 18:
               raise ValidationError(_('Please Input the proper age!'))



    # THis Part is used for the Cancel , Confirmed and Approved Button.....................

    def inventory_cancel(self, cr, uid, ids, context=None):
        if ids is not None:
            cr.execute("update inventory_item set state='cancelled' where id=%s", (ids))
            cr.commit()
        return True

    def inventory_confirm(self, cr, uid, ids, context=None):
        if ids is not None:
            cr.execute("update inventory_item set state='confirmed' where id=%s", (ids))
            cr.commit()
        return True

    def inventory_approve(self, cr, uid, ids, context=None):
        if ids is not None:
            cr.execute("update inventory_item set state='approved' where id=%s", (ids))
            cr.commit()
        return True

# This part is used for the unit price total value Function
    @api.onchange('inventory_line_id')
    def onchange_total(self):
        total = 0
        for item in self.inventory_line_id:
            total = total + item.sub_total_amount
        self.total = total

    @api.onchange('unit_price', 'quantity')
    def _onchange_sub_total_amount(self):
        for record in self:
            record.sub_total_amount = record.unit_price * record.quantity
# This part is used for the notebook item list for tree view
class inventory_information(osv.osv):
    _name = 'inventory.item.line'

    _columns = {
        'name': fields.many2one("inventory.item.entry", "Item Name", ondelete='cascade'),
        'inventory_item_id': fields.many2one('inventory.item', "Information"),
        'quantity': fields.integer(string='Quantity', default=lambda self: self._default_quantity()),
        'date': fields.date('Date'),
        'sub_total_amount': fields.integer("Sub Total Amount"),
        'unit_price': fields.integer("Unit Price"),
        'note': fields.char("Note")
    }
# This code is used for Quantity measured for the form View
    def _default_quantity(self):
        return 1
#=================================================
    # This part is used to quantity with the total amount for the every line item
    @api.onchange('unit_price', 'quantity')
    def _onchange_sub_total_amount(self):
        for record in self:
            record.sub_total_amount = record.unit_price * record.quantity
    # this code used for the  Quantity measured
    # @api.onchange('inventory_line_id')
    # def onchange_total(self):
    #     quantity = 0
    #     for item in self.inventory_line_id:
    #         total = quantity * item.obtained_marks
    #     self.total = total



# This part is used for the onchange value item of notebook

    def onchange_item(self, cr, uid, ids, name, context=None):
        tests = {'values': {}}
        dep_object = self.pool.get('inventory.item.entry').browse(cr, uid, name, context=None)
        abc = {'date': dep_object.date, 'unit_price': dep_object.obtained_marks}
        tests['value'] = abc
        return tests


# This part is used for the item add Menu
class inventory_item_config(osv.osv):
    _name = "inventory.item.entry"
    _order = 'id asc'
    _columns = {
        'name': fields.char("Product Name"),
        'date': fields.date("Date"),
        'obtained_marks': fields.float("Fee"),
    }
