{
    "name": "License OCAD",
    "summary": """
        Sync licenses with the OCAD license activation service.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["license"],
    "data": [
        "views/license_license.xml",
        "views/product_template.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"]
}