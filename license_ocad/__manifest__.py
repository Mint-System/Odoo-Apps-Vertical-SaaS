{
    "name": "License OCAD",
    "summary": """
        Sync licenses with the OCAD license activation service.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Services",
    "version": "16.0.1.3.0",
    "license": "AGPL-3",
    "depends": ["license_sale", "product_information_management"],
    "data": [
        "security/ir.model.access.csv",
        "data/product_information_attribute_data.xml",
        "views/res_config_settings.xml",
        "views/license_license.xml",
        "views/license_activation.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
