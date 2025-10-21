# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Kubectl Import",
    "summary": """
        Import data from Kubernetes cluster.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["kubectl"],
    "data": ["views/kubectl_context_views.xml", "views/kubectl_namespace_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
