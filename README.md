# Oasis Software Setup Instructions


## Table of Contents
1. [Flash Image](#flash-image)
2. [Initial SSH Connection](#initial-ssh-connection)
3. [Run Setup Script](#run-setup-script)
4. [Manual Configuration](#manual-configuration)

## Flash Image

1. Download the oasis2_small image (recommended, oasis2 will also work but takes longer) from the lab [google drive](https://drive.google.com/drive/u/0/folders/1BG0I_dm2JzCSMFcGO7WA8y0n1dVrUQpe).

2. Flash the oasis2_small image to a microSD card at least 8GB or larger using Etcher or Win32 Disk Imager (we typically use 64GB... need to test if the new smaller image works on smaller cards). Be patient, a large image can take ~1 hour to a 64GB card, the smaller image takes ~1 minute over USB3.

3. Place the card in the Raspberry Pi **WITH THE POWER OFF** (inserting or removing the card with the power on can corrupt the drive!!!).

4. Turn on the Pi. If using the smaller image it may need to power cycle a few times to expand the image, this can take a minute or two on a Pi Zero.

## Initial SSH Connection

1. Connect to the new oasis via SSH.

        ssh pi@192.168.137.2

   Password: `raspberry`

## Run Setup Script
1. Run the setup script (replace HOSTNAME, IP, DESKTOP_IP with values for your oasis, eg. oasis209, 192.168.137.209, default DESKTOP_IP is 192.168.137.22, but you should change it if the agent_tracker computer has a different IP)

        cd oasis_pi
        bash setup_oasis.sh HOSTNAME IP [DESKTOP_IP]

## Manual Configuration

This should only be necessary if the setup script failed for some reason!

### Configure IP Address

1. Open the DHCP configuration file.

        nano /etc/dhcpcd.conf

2. Set the static IP address line to the desired oasis ID (replace `XXX` with the desired oasis number, e.g. `209`).

        static ip_address=192.168.137.XXX

3. Save and close the file.

### Configure Hostname

1. Open the hostname file.

        sudo nano /etc/hostname

2. Set the hostname to match the desired oasis ID (e.g. `oasis209` if the IP address ends in `209`).

3. Save and close the file, then reboot.

        sudo reboot

### SSH Key Setup

1. If you have not yet generated an SSH key on the desktop, generate one first, then continue to step 2. Otherwise, go straight to step 2.

        ssh-keygen -t rsa -b 4096

   Press Enter to accept the default file location (`~/.ssh/id_rsa`) and optionally set a passphrase when prompted.

2. If you have already generated an SSH key on the desktop, copy it to the oasis (replace `XXX` with the oasis ID). Enter the password `raspberry` when prompted.

        ssh-copy-id pi@192.168.137.XXX



### Pull Latest Code

1. The oasis image should already contain a folder called `oasis_pi`. Navigate to it.

        cd oasis_pi

2. Pull the latest code from the `Oasis_Pi` branch of the [cellworld_habitat_pi](https://github.com/germanespinosa/cellworld_habitat_pi.git) repository.

        git pull

### Configure Desktop IP

1. Open `maze-terminal2.py` and verify that the desktop IP address is set to `192.168.137.22`. If your desktop has a different IP address, update it accordingly.

        nano maze-terminal2.py

### Configure Feeder

1. Open the feeder calibration file.

        nano feeder.cal

2. Set the file contents as follows:
    - **Line 1**: The duration in seconds required to deliver the desired reward amount. Now might be a good time to calibrate the oasis ;)
    - **Line 2**: The oasis ID number (e.g. `209` for `oasis209`).
