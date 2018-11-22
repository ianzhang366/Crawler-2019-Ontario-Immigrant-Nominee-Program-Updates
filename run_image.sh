#!/bin/bash
#this script is load the image built by build_docker_image.sh and run it

VERSION=$1;
docker run -d pnp_crawler:${VERSION}