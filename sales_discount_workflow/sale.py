# -*- coding: utf-8 -*-
# WR Ltd https://cloud.wrltd.ca

from odoo import api, fields, models, tools, _


class SaleOrder(models.Model):
    _inherit = "sale.order"


    # add new state to_approve, duplicate action_confirm button with state to_approve for group sales manager 
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to_approve', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')


    @api.multi
    def action_confirm(self):
        for order in self:
            for line in order.order_line:
                if line.discount and (line.discount > self.env.user.discount_limit):
                    order.state = 'to_approve'
                    order.confirmation_date = fields.Datetime.now()
                    res = super(SaleOrder, self).action_confirm()

        return True