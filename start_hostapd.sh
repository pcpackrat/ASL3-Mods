#!/bin/bash

# Generate the SSID based on the hostname
SSID="ASL3_${HOSTNAME}"

# Ethernet and Wi-Fi interfaces to check
ETH_INTERFACE="eth0"
WIFI_INTERFACE="wlan0"

# Write configuration to hostapd.conf
echo "interface=wlan0
driver=nl80211
ssid=${SSID}
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=YourPassword
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP" > /etc/hostapd/hostapd.conf

# Check if Ethernet is connected
ETH_CONNECTED=$(cat /sys/class/net/$ETH_INTERFACE/carrier 2>/dev/null)

# Check if wlan0 is connected to a network
WIFI_CONNECTED=$(iw dev $WIFI_INTERFACE link | grep "Connected")

# Path to the rpt_http_registration.conf file
CONF_FILE="/etc/asterisk/rpt_http_registrations.conf"

# Extract the number before the colon on the line that starts with 'register =>'
NODENUM=$(grep '^register =>' "$CONF_FILE" | sed -n 's/^register =>\s*\([0-9]*\):.*/\1/p')

# Start hostapd if either Ethernet or Wi-Fi is connected
if [[ "$ETH_CONNECTED" -eq 0 ]] && [[ -z "$WIFI_CONNECTED" ]]; then
    systemctl start hostapd
    asterisk -rx "rpt localplay $NODENUM /usr/share/asterisk/sounds/custom/wifi-disconnected"
else
    systemctl stop dnsmasq
fi
