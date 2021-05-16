# -*- coding: utf-8 -*-
# WR Ltd https://cloud.wrltd.ca
# create new security group to grant access to users

from odoo import api, fields, models, tools, _

class PosOrder(models.Model):
    _inherit = "pos.order"



    def _force_picking_done(self, picking):
        """Force picking in order to be set as done."""
        self.ensure_one()
        res = super(PosOrder, self)._force_picking_done(picking)

        if picking.state == 'assigned':
        	picking.action_pack_operation_auto_fill()
            picking.do_new_transfer()

        return res