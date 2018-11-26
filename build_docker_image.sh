#!/bin/bash
#this script is used to build the docker image from the Dockerfile 

C_NAME=$1;
VERSION=$2;

SCRIPT_START_TIME=`date`;
echo -e "\n\n Build docker image script start time: ${SCRIPT_START_TIME}";

docker build -t ${C_NAME}:${VERSION} -f /home/pnpCrawler/Dockerfile . 

SCRIPT_COMPLETE_TIME=`date`;
echo -e "\n\n Build docker image script complete time: ${SCRIPT_COMPLETE_TIME}";
