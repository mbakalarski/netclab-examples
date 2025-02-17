version=$(basename $(curl -s -w "%{redirect_url}" https://github.com/open-traffic-generator/otgen/releases/latest) | cut -c 2-)
curl -sLO https://github.com/open-traffic-generator/otgen/releases/download/v${version}/checksums.txt
curl -sLO https://github.com/open-traffic-generator/otgen/releases/download/v${version}/otgen_${version}_Linux_x86_64.tar.gz

sha256sum --check --ignore-missing checksums.txt
tar xvzf otgen_${version}_Linux_x86_64.tar.gz otgen

chmod +x otgen
alias otgen="./otgen"
. <(otgen completion bash)

rm otgen_${version}_Linux_x86_64.tar.gz
rm checksums.txt
