#!/bin/bash
#this script is load the image built by build_docker_image.sh and run it

VERSION=$1;
#adding the project to image
docker run -dit -p 8888:8888 pnp_crawler:${VERSION}
