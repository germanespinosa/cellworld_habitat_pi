#!/bin/bash
if grep -q $'\r$' "$0"; then sed -i 's/\r$//' "$0"; exec bash "$0" "$@"; fi # Fix Windows line endings

# Usage: bash setup_oasis.sh HOSTNAME IP [DESKTOP_IP]
# Run as your normal Pi user, without sudo.
# Assumes ~/oasis_pi, dhcpcd, and one existing static IP setting.

HOST=${1:?Usage: bash setup_oasis.sh HOSTNAME IP [DESKTOP_IP]}
IP=${2:?Provide the target IP address}
DESKTOP_IP=${3:-192.168.137.22}

[[ $HOST =~ ^oasis[0-9]+$ ]] || {
    echo "Hostname must look like oasis209."
    exit 1
}
ID=${HOST#oasis}

valid_ip() {
    local part
    local -a parts
    [[ $1 =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
    IFS=. read -ra parts <<< "$1"
    for part in "${parts[@]}"; do
        (( 10#$part <= 255 )) || return 1
    done
}

valid_ip "$IP" && valid_ip "$DESKTOP_IP" || {
    echo "Invalid IP address."
    exit 1
}

cd "$HOME/oasis_pi"

[[ $(git rev-parse --abbrev-ref HEAD) == Oasis_Pi ]] || {
    echo "Switch to the Oasis_Pi branch first."
    exit 1
}

[[ -s feeder.cal ]] || {
    echo "feeder.cal is missing or empty. Calibrate the feeder first."
    exit 1
}

# Stop if the network configuration isn't the simple expected layout.
COUNT=$(grep -Ec '^[[:space:]]*static[[:space:]]+ip_address=' \
    /etc/dhcpcd.conf || true)
[[ $COUNT == 1 ]] || {
    echo "Expected one static ip_address line in /etc/dhcpcd.conf."
    echo "Please configure the correct interface manually."
    exit 1
}

sudo -v
BACKUP=$(mktemp -d "$HOME/oasis-backup.XXXXXX")
cp feeder.cal maze-terminal2.py "$BACKUP/"
sudo cp /etc/dhcpcd.conf /etc/hostname /etc/hosts "$BACKUP/"
echo "Backups: $BACKUP"

# Preserve calibration even if Git supplies new default values.
trap 'cp "$BACKUP/feeder.cal" feeder.cal' EXIT
git pull --ff-only origin Oasis_Pi
cp "$BACKUP/feeder.cal" feeder.cal
trap - EXIT

# Change only the ID on line 2; preserve duration and any other lines.
if [[ $(awk 'END {print NR}' feeder.cal) -lt 2 ]]; then
    echo "feeder.cal needs a duration on line 1 and ID on line 2."
    exit 1
fi
sed -i "2c\\$ID" feeder.cal

# Replace the documented desktop address if a different one is supplied.
if [[ $DESKTOP_IP != 192.168.137.22 ]]; then
    grep -qF '192.168.137.22' maze-terminal2.py || {
        echo "Desktop IP is not the expected 192.168.137.22."
        echo "Edit maze-terminal2.py manually, then rerun."
        exit 1
    }
    sed -i "s/192\.168\.137\.22/$DESKTOP_IP/g" maze-terminal2.py
fi

# Preserve an existing subnet prefix, such as /24.
sudo sed -i -E \
    "s|^([[:space:]]*static[[:space:]]+ip_address=)[0-9.]+|\1$IP|" \
    /etc/dhcpcd.conf

printf '%s\n' "$HOST" | sudo tee /etc/hostname >/dev/null

if grep -qE '^127\.0\.1\.1[[:space:]]' /etc/hosts; then
    sudo sed -i -E \
        "s/^(127\.0\.1\.1[[:space:]]+)[^[:space:]]+/\1$HOST/" \
        /etc/hosts
else
    printf '127.0.1.1\t%s\n' "$HOST" | sudo tee -a /etc/hosts >/dev/null
fi

echo "Setup complete. Feeder duration preserved."
echo "When ready, run: sudo reboot"
echo "Then reconnect to $IP."
