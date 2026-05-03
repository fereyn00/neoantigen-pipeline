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

    docker image inspect netchop_image:latest --format '{{.Architecture}}' | grep -qx amd64
    docker image inspect netmhcpan_image:latest --format '{{.Architecture}}' | grep -qx arm64

    touch docker_images.ready
    """
}
