#!/bin/bash

###############################
#### Install docker
sudo pacman -S docker

# Start docker and enable it to run at startup
sudo systemctl start docker.service
sudo systemctl enable docker.service

# Enable current user to run docker as superuser
sudo usermod -aG docker $USER

# Reboot system

################################
#### Install portainer
cd ~
mkdir -p ~/app_config/portainer
docker pull portainer/portainer-ce
#Create the container pointing to docker service
docker run -d -p 8000:8000 -p 9443:9443 --restart=always \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v ~/apps/portainer/:/data \
	--name "portainer" portainer/portainer-ce:latest
#In order to connect go to https://localhost:9443
