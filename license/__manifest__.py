{
    "name": "License Management",
    "summary": """
        Manage software licensens.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Services",
    "version": "18.0.1.0.0",
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
