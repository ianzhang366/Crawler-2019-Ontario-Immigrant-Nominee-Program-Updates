#!/bin/bash
#this script is load the image built by build_docker_image.sh and run it
echo -e 'Need 2 parameters to run.\n Para1: indicate the image version. \n Para2: indicate the container name.\n'

C_NAME=$1;
VERSION=$2;

echo -e "Version: ${VERSION} \t C_NAME: ${C_NAME}"
#adding the project to image
docker ps 
if docker ps --filter "name=${C_NAME}" | grep -i "${C_NAME}"; then
	echo -e "Killing the previous running container"
	docker kill ${C_NAME}
	echo -e "Removing /${C_NAME}"
	docker rm "/${C_NAME}"
fi 
docker run -dit -p 8888:8888 --name "${C_NAME}_${VERSION}" ${C_NAME}:${VERSION}
docker ps --filter "name=${C_NAME}"
