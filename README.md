# Oasis Software Setup Instructions


## Table of Contents
1. [Flash Image](#flash-image)
2. [Initial SSH Connection](#initial-ssh-connection)
3. [Configure IP Address](#configure-ip-address)
4. [Configure Hostname](#configure-hostname)
5. [SSH Key Setup](#ssh-key-setup)
6. [Pull Latest Code](#pull-latest-code)
7. [Configure Desktop IP](#configure-desktop-ip)
8. [Configure Feeder](#configure-feeder)

## Flash Image

1. Flash the oasis201 image to a black 64GB SD card using Etcher or Win32 Disk Imager.

## Initial SSH Connection

1. Connect to the new oasis via SSH using the default credentials.

        ssh pi@192.168.137.201

   Password: `raspberry`

## Configure IP Address

1. Open the DHCP configuration file.

        nano /etc/dhcpcd.conf

2. Set the static IP address line to the desired oasis ID (replace `XXX` with the desired oasis number, e.g. `209`).

        static ip_address=192.168.137.XXX

3. Save and close the file.

## Configure Hostname

1. Open the hostname file.

        sudo nano /etc/hostname

2. Set the hostname to match the desired oasis ID (e.g. `oasis209` if the IP address ends in `209`).

3. Save and close the file, then reboot.

        sudo reboot

## SSH Key Setup

1. If you have not yet generated an SSH key on the desktop, generate one first, then continue to step 2. Otherwise, go straight to step 2.

        ssh-keygen -t rsa -b 4096

   Press Enter to accept the default file location (`~/.ssh/id_rsa`) and optionally set a passphrase when prompted.

2. If you have already generated an SSH key on the desktop, copy it to the oasis (replace `XXX` with the oasis ID). Enter the password `raspberry` when prompted.

        ssh-copy-id pi@192.168.137.XXX



## Pull Latest Code

1. The oasis image should already contain a folder called `oasis_pi`. Navigate to it.

        cd oasis_pi

2. Pull the latest code from the `Oasis_Pi` branch of the [cellworld_habitat_pi](https://github.com/germanespinosa/cellworld_habitat_pi.git) repository.

        git pull

## Configure Desktop IP

1. Open `maze-terminal2.py` and verify that the desktop IP address is set to `192.168.137.22`. If your desktop has a different IP address, update it accordingly.

        nano maze-terminal2.py

## Configure Feeder

1. Open the feeder calibration file.

        nano feeder.cal

2. Set the file contents as follows:
    - **Line 1**: The duration in seconds required to deliver the desired reward amount. Now might be a good time to calibrate the oasis ;)
    - **Line 2**: The oasis ID number (e.g. `209` for `oasis209`).
