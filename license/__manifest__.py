{
    "name": "License Management",
    "summary": """
        Manage software licensens.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.3.0",
    "license": "AGPL-3",
    "depends": ["base", "product"],
    "data": [
        "views/license_license.xml",
        "views/license_type.xml",
        "security/security.xml",
        "data/ir_sequence.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
