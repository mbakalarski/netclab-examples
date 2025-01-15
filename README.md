# network-tests

This is collection of network tests.<br>
Testbeds are defined via k8s manifest files.

## Prerequisites
* Linux host or VM
* Docker (rootless mode)
* Python 3.x

## Tools
* Install kubectl and kind tool, e.g.
```
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```
```
version=$(basename $(curl -s -w %{redirect_url} https://github.com/kubernetes-sigs/kind/releases/latest))
curl -Lo ./kind https://kind.sigs.k8s.io/dl/${version}/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```
* Run vLab installation script:
```
bash <(curl -Ls "https://raw.githubusercontent.com/mbakalarski/vLab/main/vlab_install.sh") kubevirt
```
or
```
bash <(curl -Ls "https://raw.githubusercontent.com/mbakalarski/vLab/main/vlab_install.sh") nokubevirt
```
* Expose images for VM routers, e.g.:
```
docker run --name www -dt --mount type=bind,source=$HOME/images,target=/usr/share/nginx/html -p 8080:80 nginx:latest
```

* Clone this repo or install the package from PyPI

## Deploy lab and run tests
* Create topology:
```
kubectl apply [-f|-k] <manifests for testbed>
```
* Run tests:
```
pytest -W "ignore::DeprecationWarning"
```
or 
```
pytest --pyargs network-tests -W "ignore::DeprecationWarning"
```
