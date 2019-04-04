#!/usr/bin/env python3

#
# Script to dowload the latest neo4j Dockerfile
#

import sys
import os
import requests
import shutil
import gzip
import stat


def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'w') as f:
        f.write(r.text)
    return local_filename


if len(sys.argv) != 2:
    NEO4J_VERSION = "3.2.5"
else:
    NEO4J_VERSION = sys.argv[1]

os.makedirs(os.path.join(NEO4J_VERSION, 'local-package'), exist_ok=True)
os.system('touch ' + os.path.join(NEO4J_VERSION, 'local-package', '.sentinel'))
os.chdir(NEO4J_VERSION)

docker_file_url = f"https://raw.githubusercontent.com/neo4j/docker-neo4j-publish/master/{NEO4J_VERSION}/community/Dockerfile"
docker_entrypoint_url = f"https://raw.githubusercontent.com/neo4j/docker-neo4j-publish/master/{NEO4J_VERSION}/community/docker-entrypoint.sh"

download_file(docker_file_url)
download_file(docker_entrypoint_url)

shutil.copyfile('Dockerfile', 'Dockerfile.orig')
os.chmod('docker-entrypoint.sh', 0o755)
os.chdir('..')
os.system(f'patch -u {NEO4J_VERSION}/Dockerfile Dockerfile.diff')
