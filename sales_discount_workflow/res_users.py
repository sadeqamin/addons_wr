# -*- coding: utf-8 -*-
# WR Ltd https://cloud.wrltd.ca

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp

class Users(models.Model):
    _inherit = "res.users"
    
    sale_order_can_approve = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Can Approve Sale?',default='no')
    discount_limit = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)