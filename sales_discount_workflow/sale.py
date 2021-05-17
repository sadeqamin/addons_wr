# -*- coding: utf-8 -*-
# WR Ltd https://cloud.wrltd.ca

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp

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
    user_can_approve_so = fields.Boolean(compute='_compute_can_approve_so', readonly=True, default=False, copy=False)
    can_approve_user_id = fields.Many2one('res.users', compute='_default_so_approval_assign', string='Request Approval From')
    #order_total_discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)
    


#    @api.multi
#    def _users_can_approve_so(self):
#        order_discount = 0.0
#        users_can_approve_so = []
#        domain = [('id', 'in', [])]
#        for order in self:
#            for line in order.order_line:
#                if line.discount:
#                    order_discount += line.discount
#            if order_discount:
#                users_can_approve_so = self.env['res.users'].sudo().search([('discount_limit', '>', int(order_discount))])
#                if users_can_approve_so:
#                    domain = [('id', 'in', users_can_approve_so.ids)]
#        print("##############################")
#        print(self.env.context)
#        print(domain)
#        return(domain)



    @api.multi
    def _compute_can_approve_so(self):
        order_discount = 0
        for order in self:
            for line in order.order_line:
                if line.discount:
                    order_discount += line.discount
            if self.env.user.discount_limit:
                if int(self.env.user.discount_limit) > int(order_discount):
                    order.user_can_approve_so = True
                else:
                    order.user_can_approve_so = False


        
        return(order.user_can_approve_so)


    @api.multi
    def _default_so_approval_assign(self):
        order_discount = 0.0
        for order in self:
            for line in order.order_line:
                if line.discount:
                    order_discount += line.discount
            if order_discount and not order.user_can_approve_so:
                can_approve_default_assign = self.env['res.users'].sudo().search([('discount_limit', '>', order_discount)], limit=1)
                if can_approve_default_assign:
                    order.can_approve_user_id = can_approve_default_assign
            

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        order_discount = 0.0
        for order in self:
            if not order.user_can_approve_so:
                order.state = 'to_approve'
                if order.can_approve_user_id:
                    order.approval_request_notification()

        return res

    @api.multi
    def action_approve_so(self):
        for order in self:
            order.action_confirm()

    @api.multi
    def approval_request_notification(self):
        template = self.env['mail.template'].search([('model', '=', 'sale.order'), ('name', '=', 'Sale order Approval Notification')], limit=1)
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return True

