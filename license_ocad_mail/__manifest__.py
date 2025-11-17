{
    "name": "License OCAD Mail",
    "summary": """
        Mail templates for OCAD.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Services",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["license_ocad", "license_subscription"],
    "data": [
        "data/mail_templates.xml",
        "views/sale_order.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
