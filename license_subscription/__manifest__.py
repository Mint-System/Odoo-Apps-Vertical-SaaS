{
    "name": "License Management Subscription",
    "summary": """
        Update license based on subscription changes.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Services",
    "version": "18.0.1.0.0",
    "license": "OPL-1",
    "depends": [
        "license_sale",
        "sale_triple_discount",
        "sale_subscription",
        "sale_order_line_pricelist_fixed_discount",
    ],
    "data": ["views/sale_subscription_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
