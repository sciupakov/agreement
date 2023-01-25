# Copyright 2023 - Andrej Ščiupakov
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Agreement"

    number = fields.Char(string='Agreement number', required=True, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    kind_id = fields.Many2one('agreement.type', string='Agreement type', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_agreement', 'In agreement'),
        ('active', 'Active'),
        ('finished', 'Finished')],
        string='State', default='draft', required=True)
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user)

    current_uid = fields.Many2one('res.users', compute='get_current_uid', string='Current user id')

    def get_current_uid(self):
        if self.env.context.get('uid', False):
            uid = self.env.context.get('uid', False)
            self.current_uid = self.env['res.users'].browse(uid)
        else:
            self.current_uid = False

    '''Agreement number is generated from ir.sequence here'''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('number') or vals['number'] == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code('agreement.number') or _('New')
        return super(Agreement, self).create(vals_list)

    def action_send_for_approval(self):
        self.ensure_one()
        self.sudo().state = 'in_agreement'

    def action_approve(self):
        self.ensure_one()
        self.sudo().state = 'active'

    def action_send_back(self):
        self.ensure_one()
        self.sudo().state = 'draft'
