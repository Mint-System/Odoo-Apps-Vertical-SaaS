{
    "name": "Website Sale Helm",
    "summary": """
        Apply Helm Charts when a product is bought.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_sale", "sale_helm"],
    "data": ["views/website_templates.xml", "data/data.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
