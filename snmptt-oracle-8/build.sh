#!/usr/bin/env bash 

set -xe

DOCKER_IMAGE=`cat podmanimage`
echo "${DOCKER_IMAGE}"
stat podmanimage && \
	( podman image inspect  "${DOCKER_IMAGE}" || buildah bud -t "${DOCKER_IMAGE}" . )
podman run -it -v `pwd`/srv:/srv "${DOCKER_IMAGE}"

set +xe
