{
    "name": "License Management",
    "summary": """
        Manage software licensens.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "views/license_license.xml",
        "views/license_type.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
