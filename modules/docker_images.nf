process ENSURE_DOCKER_IMAGES {

    tag "docker-images"
    cache false

    output:
    path("docker_images.ready")

    script:
    """
    set -euo pipefail

    docker build --platform linux/amd64 -t netchop_image:latest ${projectDir}/docker/netchop

    docker build --platform linux/arm64/v8 -t netmhcpan_image:latest ${projectDir}/docker/netmhcpan

    docker build --platform linux/amd64 -t mhcflurry_image:latest ${projectDir}/docker/mhcflurry

    docker build --platform linux/amd64 -t mixmhcpred_image:latest ${projectDir}/docker/mixmhcpred

    docker image inspect netchop_image:latest --format '{{.Architecture}}' | grep -qx amd64
    docker image inspect netmhcpan_image:latest --format '{{.Architecture}}' | grep -qx arm64
    docker image inspect mhcflurry_image:latest --format '{{.Architecture}}' | grep -qx amd64
    docker image inspect mixmhcpred_image:latest --format '{{.Architecture}}' | grep -qx amd64

    touch docker_images.ready
    """
}
