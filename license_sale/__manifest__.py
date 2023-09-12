{
    "name": "License Management Sale",
    "summary": """
        Sell software licenses.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.1.1",
    "license": "AGPL-3",
    "depends": ["license", "sale"],
    "data": [
        "views/product_template.xml",
        "views/license_license.xml",
        "views/sale_order.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
