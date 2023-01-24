# Copyright 2023 - Andrej Ščiupakov
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class AgreementType(models.Model):
    _name = "agreement.type"
    _inherit = ['mail.thread']
    _description = "Agreement Type"

    name = fields.Char(string="Name", required=True, tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)

    _sql_constraints = [('type_name_uniq', 'unique (name)', 'The name of an agreement type must be unique!')]
