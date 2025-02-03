# netclab-examples

Here is some Python code and YAML files for network tests.<br>
Topologies are defined in K8S manifests.

## Prerequisites
* Linux host or VM
* netclab installed (https://github.com/mbakalarski/netclab)
* Python 3.x

## Install netclab-examples
```
git clone https://github.com/mbakalarski/netclab-examples.git
cd netclab-examples
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run topology and tests
Deploy topology:
```
kubectl apply [-f|-k] <manifests for topology>
```
or
```
tools/apply_delete_topology.sh apply <topology_dir>
```
e.g.
```
tools/apply_delete_topology.sh apply topo-02
```

Add vars to ```.env``` file, e.g.:
```
cat << EOF > .env
K8S_NAMESPACE="default"
IMAGES_DIR="${HOME}/images"
CSR_USER="netclab"
CSR_PASS="cisco"
EOF
```

Run tests:
```
pytest --pyargs netclab-examples
```
