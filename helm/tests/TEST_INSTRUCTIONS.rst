Prepare Kubernetes:

- Start local kind cluster "kind-kind"
- Add the "kubernetes-build", "ingress-nginx" and "cnpg" repos
- Setup hostnames cloud.local, odoo.cloud.local, restic.local and restic.cloud.local

Install ingress-nginx chart

- Open "Helm > Charts > ingress-nginx" and click "Release"
- Enter name "ingress-nginx" and select "loc" as context
- Create namespace "ingress-nginx"
- Select customer "Mint System"
- Confirm and install release
- Refresh page and check if it was installed

Install cloudnative-pg chart

- Open "Helm > Charts > cloudnative-pg" and click "Release"
- Enter name "cloudnative-pg" and select "kind-kind" as context
- Create namespace "cnpg-system"
- Select customer "Mint System"
- Confirm and install release
- Refresh page and check if it was installed

Install odoo chart

- Open "Helm > Charts > odoo" and click "Release"
- Enter name "odoo" and select "kind-kind" as context
- Create namespace "odoo"
- Select customer "Mint System"
- Confirm and install release
- Refresh page and check if it was installed

Uninstall charts

- Open "Helm > Releases > odoo" and click "Uninstall"
- Open "ingress-nginx" release and click "Uninstall"
- Open "cloudnative-pg" release and click "Uninstall"
