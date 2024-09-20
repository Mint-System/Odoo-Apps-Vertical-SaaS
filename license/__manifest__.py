{
    "name": "License Management",
    "summary": """
        Manage software licensens.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.4.0",
    "license": "AGPL-3",
    "depends": ["base", "product"],
    "data": [
        "security/security.xml",
        "views/license_license.xml",
        "views/license_type.xml",
        "views/res_partner.xml",
        "data/ir_sequence.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
