{
    'name': "Agreement",
    'version': '16.0',
    'depends': ['base', 'mail', 'contacts'],
    'author': "Andrej Ščiupakov",
    'license': 'AGPL-3',
    'description': """
    Test task module
    """,
    'installable': True,
    'application': True,
    'data': [
        "data/ir_sequence_data.xml",
        "data/ir_cron.xml",
        "data/mail_templates.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/agreement.xml",
        "views/agreement_type.xml",
        "views/agreement_menus.xml",
    ]
}