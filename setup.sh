#!/bin/bash
# this script is used to install docker and docker-compose on the test vm for running the project later on
install_docker() {
		echo -e "\n\nInstalling Docker\n";
		curl -fsSL get.docker.com -o get-docker.sh;
		sh get-docker.sh;
		rm get-docker.sh;
}

install_docker_compose() {
		echo -e "\n\nInstalling Docker-Compose\n";
		sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose;
		sudo chmod +x /usr/local/bin/docker-compose;
}


main() {
		ENV=$1;
		VERSION_WITH_PERIODS=$2;
        echo -e "$1\t$2"
		SCRIPT_START_TIME=`date`;
		
		install_docker
		install_docker_compose

		
		SCRIPT_END_TIME=`date`;
		echo -e "\n\nScript Start Time: ${SCRIPT_START_TIME}";
		echo -e "Script End Time: ${SCRIPT_END_TIME}";
		echo -e "\n\n\nProject ENV Set up Completed.\n";
}

main "$1" "$2"