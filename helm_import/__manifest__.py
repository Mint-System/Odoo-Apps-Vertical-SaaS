# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helm Import",
    "summary": """
        Import data from Helm repo.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["helm"],
    "data": ["views/helm_repo_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
