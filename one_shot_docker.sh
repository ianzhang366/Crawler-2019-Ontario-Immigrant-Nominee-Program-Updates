#!/bin/bash
#this script is used to build and run a docker image from the Dockerfile 

printUsage () {

  echo " ---------------------------------------------------------------------------"
  echo "  This script is used to build and run a docker image from the Dockerfile "
  echo "  Need 2 parameters to run"
  echo " Para1 indicates the image name"
  echo " Para2: indicate the image version"
  echo " ---------------------------------------------------------------------------"
  return 0; }


build_run(){

    echo -e "Version: ${VERSION} \t C_NAME: ${C_NAME}"

    SCRIPT_START_TIME=`date`;
    echo -e "\n\n Build docker image script start time: ${SCRIPT_START_TIME}";

    docker build -t ${C_NAME}:${VERSION} -f /home/pnpCrawler/Dockerfile . 

    SCRIPT_COMPLETE_TIME=`date`;
    echo -e "\n\n Build docker image script complete time: ${SCRIPT_COMPLETE_TIME}";



    SCRIPT_COMPLETE_TIME=`date`;
    echo -e "\n\n Start docker image: ${SCRIPT_COMPLETE_TIME}";

    #kill container, since we only expose 1 port
    if docker ps --filter "name=${C_NAME}" | grep -ic "${C_NAME}"; then
        docker kill $(docker ps -q)
    fi 
    docker run -dit -p 8888:8888 --name "${C_NAME}_${VERSION}" ${C_NAME}:${VERSION}

    docker ps  --filter "name=${C_NAME}" --format "table {{.ID}}\t{{.Image}}\t{{.CreatedAt}}" 

    SCRIPT_COMPLETE_TIME=`date`;
    echo -e "\n\n Docker imag e${C_NAME}:${VERSION} started at: ${SCRIPT_COMPLETE_TIME}";
}

#-------------------------------------------
# main
#-------------------------------------------

C_NAME=$1;
VERSION=$2;

if [ -z "$1" || "$2"] ; then
    printUsage
    exit 1
fi
build_run