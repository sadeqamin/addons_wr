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
    user_can_approve_so = fields.Boolean(compute='_compute_can_approve_so', readonly=True, default=False)
    can_approve_user_id = fields.Many2one('res.users', string='Request Approval From')

    @api.multi
    def _compute_can_approve_so(self):
        order_discount = 0.0
        for order in self:
            for line in order.order_line:
                if line.discount:
                    order_discount += line.discount
            can_approve_so_user_ids = self.env['res.users'].sudo().search([('sale_order_can_approve', '=', True), ('discount_limit', '>=', order_discount)])
            order.can_approve_user_id = can_approve_so_user_ids[0]
            if self.env.user in can_approve_so_user_ids:
                order.user_can_approve_so = True

    @api.multi
    def action_request_approval(self):
        for order in self:
            order.state = 'to_approve'
            order.approval_request_notification()
        return {}


#    @api.multi
#    def action_request_approved(self):
#        for order in self:
#            order.action_confirm()

    @api.multi
    def approval_request_notification(self):
        self.ensure_one()
        template = self.env['mail.template'].search([('model', '=', 'sale.order'), ('subject', '=', 'Sale Order Approval Request')], limit=1)
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return True