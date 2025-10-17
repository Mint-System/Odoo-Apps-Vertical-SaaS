Prepare Kubernetes:

- Start local kindd cluster "kind-kind"
- Setup hostnames cloud.local, odoo.cloud.local, restic.local and restic.cloud.local

Check repo:

- Open "Helm > Repos" and click on "kubernetes-build"
- Ensure the repo has been added
- Repeate the same for "ingress-nginx" and "cnpg"

Install ingress-nginx and cnpg chart

- Open "Helm > Charts > ingress-nginx" and click "Release"
- Enter name "ingress-nginx" and select "loc" as context
- Select customer "Mint System"
- Confirm and install release
- Refresh page and check if it was installed
- Repeat the same for cnpg

Install odoo chart

- Open "Helm > Charts > odoo" and click "Release"
- Enter name "odoo" and select "loc" as context
- Create namespace "odoo"
- Select customer "Mint System"
- Confirm and install release
- Refresh page and check if it was installed

Uninstall charts

- Open "Helm > Releases > odoo" and click "Uninstall"
- Open "ingress-nginx" release and click "Uninstall"
