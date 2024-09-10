{
    "name": "License Management Website",
    "summary": """
        Portal view for licenses.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["license", "portal"],
    "data": [
        "views/license_portal.xml",
        "views/license_license.xml",
        "views/website_sale_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
