{
    "name": "License Management Subscription",
    "summary": """
        Update license based on subscription changes.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["license_sale", "sale_subscription"],
    "data": ["views/license_license_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
