# Copyright 2023 - Andrej Ščiupakov
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Agreement"

    number = fields.Char(string='Agreement number',
                         required=True,
                         readonly=True,
                         tracking=True,
                         default=lambda self: self.env['ir.sequence'].next_by_code('agreement.number'))
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, tracking=True)
    kind_id = fields.Many2one('agreement.type', string='Agreement type', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_agreement', 'In agreement'),
        ('active', 'Active'),
        ('finished', 'Finished')],
        string='State', default='draft', required=True, tracking=True)
    start_date = fields.Date(string='Start date', required=True, tracking=True)
    end_date = fields.Date(string='End date', required=True, tracking=True)
    author_id = fields.Many2one('res.users', string='Author', tracking=True, default=lambda self: self.env.user)

    show_button = fields.Boolean(compute='_compute_show_button', string='Show button', readonly=True)

    def get_current_uid(self):
        if self.env.context.get('uid', False):
            uid = self.env.context.get('uid', False)
            self.current_uid = self.env['res.users'].browse(uid)
        else:
            self.current_uid = False

    def action_send_for_approval(self):
        self.ensure_one()
        self.state = 'in_agreement'

    def action_approve(self):
        self.ensure_one()
        self.state = 'active'

    def action_send_back(self):
        self.ensure_one()
        self.state = 'draft'
        # send notification to author
        self.message_post(body=_('Agreement %s was sent back for revision.'))

    @api.depends('author_id', 'state')
    def _compute_show_button(self):
        for rec in self:
            rec.show_button = self.env.user.id == rec.author_id.id and rec.state == 'draft'

    def _finish_agreements(self):
        # This method is called from cron job
        agreements = self.search([('state', '=', 'active'), ('end_date', '<', fields.Date.today())])
        if agreements:
            agreements.write({'state': 'finished'})
