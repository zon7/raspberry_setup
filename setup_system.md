# Environment configuration

# 1. BTRFS setup
If BTRFS drive already exists jump to 1.2.

If BTRFS is not installed, install it with
>
    sudo apt install btrfs-progs

## 1.1 Create BTRFS setup
View available disks with any of this tools
>
    sudo lsblk
    sudo blkid

To create a RAID-1 with two disks use the next command
>
    sudo mkfs.btrfs -L <Label> -m raid1 -d raid1 /dev/<disk1> /dev/<disk2> ....

If needed add the **-f** option 

## 1.2 Mount BTRFS drive
First get the BTRFS drive UUID with **blkid** command, or with the help of btrfs tools
>
    sudo btrfs device scan
    sudo btrfs filesystem show

In order to get the UUID you can use blkid.

Then create the mount point

    sudo mkdir -p /mnt/NAS
    sudo chmod 777 /mnt/NAS
    or 
    sudo chown -R pi /mnt/NAS

Then add the needed line to fstab
>
    sudo vim /etc/fstab
    #Add this at the end of the file
    UUID=<Device UUID> /mnt/NAS btrfs defaults,autodefrag 0 0 

To finish just mount the drive and check it
>
    sudo mount --all
    df
    ls /mnt/NAS

# 1.3 BTRFS problems
Useful commands
>
    btrfs filesystem show # Shows all filesys and devices
    btrfs filesystem df
    
To check the filesystem usage
>
    btrfs filesystem usage /mnt/NAS

If some data is missing (Device missing) just fix it telling btrfs to use the unused space.
>
    btrfs filesystem resize max /mnt/NAS

# 2. Basic Raspberry setup

## 2.1 Needed tools
Enable SSH if not enabled
>
    sudo systemctl enable ssh
    sudo systemctl start ssh



## 2.2 Setup mDNS/Zeroconf
This will allow us to access the machine by machine name instead of the IP (eg zon7pi.local).
>
    # Install avahi
    apt install avahi-daemon
    # Start and enable the service
    systemctl start avahi-daemon

Last thing to do is enabling the mDNS. Edit /etc/nsswitch.conf
and in the hosts line add this before resolve and dns.

     mdns_minimal [NOTFOUND=return]

After this, you should be able to ping the machine by hostname.local and acces urls by hostname.local

# 3. Install container management
## 3.1 Install docker

    arch > sudo pacman -S docker
    debian > sudo apt install docker


Enable docker to be run by current user (must be a sudoer)

    sudo usermod -aG docker $USER

Enable docker to run on startup
>
    sudo systemctl start docker.service
    sudo systemctl enable docker.service

## 3.2 Install portainer
First create portainer data folder
>
    mkdir -p ~/app_config/portainer
    docker pull portainer/portainer-ce

Then create the portainer docker
>
    docker run -d -p 8000:8000 -p 9443:9443 --restart=always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v ~/apps/portainer/:/data \
        --name "portainer" portainer/portainer-ce:latest

In order to connect navigate to
https://localhost:9443


# 4. Install containers
## 4.1 QBittorrent
From portainer create a new stack and paste this:
- Fix PUID and PGID to match current user (use "id" command from terminal)
- Fix TZ if needed
- Fix /config and /downloads path to match your folder structure

>
    ---
    # Connect on localhost:8080
    version: "2.1"
    services:
        qbittorrent:
            image: lscr.io/linuxserver/qbittorrent
            container_name: qbittorrent
            environment:
                - PUID=1000
                - PGID=1000
                - TZ=Europe/Madrid
                - WEBUI_PORT=8080
            volumes:
                - /mnt/NAS/app_data/qbittorrent:/config
                - /mnt/NAS/downloads:/downloads
            ports:
                - 6881:6881
                - 6881:6881/udp
                - 8080:8080
            restart: unless-stopped

To access go to http://localhost:8080

Default credentials admin/adminadmin


## 4.2 Plex
From portainer paste this:
- To fill PLEX_CLAIM go to http://plex.tv/claim

>
    ---
    # Connect on localhost:32400/web
    version: "2.1"
    services:
        plex:
            image: lscr.io/linuxserver/plex
            container_name: plex
            network_mode: host
            environment:
            - PUID=1000
            - PGID=1000
            - VERSION=docker
            - PLEX_CLAIM= #NEEDED VALUE
            volumes:
            - /mnt/NAS/app_data/plex:/config
            - /mnt/NAS/downloads/tv:/tv
            - /mnt/NAS/downloads/movies:/movies
            restart: unless-stopped

To connect go to http://localhost:32400/web

