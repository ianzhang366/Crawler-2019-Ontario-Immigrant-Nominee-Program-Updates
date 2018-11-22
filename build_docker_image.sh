#!/bin/bash
#this script is used to build the docker image from the Dockerfile 

VERSION=$1;
SCRIPT_START_TIME=`date`;
echo -e "\n\n Build docker image script start time: ${SCRIPT_START_TIME}";

docker build -t pnp_crawler:${VERSION} -f /home/pnpCrawler/Dockerfile . 

SCRIPT_COMPLETE_TIME=`date`;
echo -e "\n\n Build docker image script start time: ${SCRIPT_COMPLETE_TIME}";
