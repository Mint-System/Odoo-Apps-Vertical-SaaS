{
    "name": "License Management Sale",
    "summary": """
        Sell software licenses.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Services",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "license",
        "sale_order_comment",
        "sale_order_line_form_action",
        "sale_order_line_pricelist_fixed_discount",
        "sale_management",
    ],
    "data": [
        "views/product_template.xml",
        "views/license_license.xml",
        "views/sale_order.xml",
        "views/sale_portal_templates.xml",
        "report/sale_report_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
