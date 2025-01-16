# network-tests

This is collection of network tests.<br>
Topologies are defined via k8s manifest files.

## Prerequisites
* Linux host or VM
* netclab installed (https://github.com/mbakalarski/netclab)
* Python 3.x

## Install network-tests
```
pip install network-tests@git+https://github.com/mbakalarski/network-tests
```
or
```
git clone https://github.com/mbakalarski/network-tests.git
pip install -e ./network-tests
```

## Run lab and tests
Deploy topology:
```
kubectl apply [-f|-k] <manifests for topology>
```

Run tests:
```
pytest --pyargs network-tests
```
or
```
pytest
``` 
