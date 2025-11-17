{
    "name": "License Website Sale",
    "summary": """
        Purchase licenses in the Odoo shop.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Services",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "license_sale",
        "website_sale",
        "website_sale_pricelist_fixed_discount",
    ],
    "data": ["views/sale_order.xml", "views/website_templates.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
