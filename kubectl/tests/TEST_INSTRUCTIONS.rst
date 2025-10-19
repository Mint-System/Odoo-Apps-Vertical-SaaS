Prepare Kubernetes:

- Start local cluster "kind-kind"

Test localhost connection:

- Open kubectl app
- Open the "loc" cluster and click "Test Connection"
- Enter "kubectl --help" as command and click run
- Check if output is given

Test with config:

- Generate kubeconfig `kubectl config view --minify --raw`
- Paste into config tab of "loc" context
- Delete the localhost kubeconfig
- Click "Test Connection"

Get namespaces:

- Open "kubectl > Namespaces".
- Mark the first entry
- Run action "Get Namespaces"
