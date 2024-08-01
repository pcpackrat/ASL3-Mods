Start with asl3 pi image

run raspi-config and set the wifi region to US

# Install some things:
sudo apt-get install hostapd dnsmasq telnet traceroute git php libapache2-mod-php openvpn

# Set openvpn to start at boot:
systemctl enable openvpn-client@client

# Copy openvpn web upload from git:
/var/www/html/vpn.html
/var/www/html/upload.php

# change group of /etc/openvpn/client to www-data and add write permission to group
chown root.www-data /etc/openvpn/client
chmod g+w /etc/openvpn/client

# Allow www-data to access network devices:
usermod -aG netdev www-data

# add to sudo using visudo:
www-data ALL=(ALL) NOPASSWD: /sbin/iwlist
www-data ALL=(ALL) NOPASSWD: /usr/bin/nmcli
www-data ALL=(ALL) NOPASSWD: /usr/sbin/reboot



Copy autoAP script from git:
/usr/local/bin/start_hostapd.sh

# Copy AutoAP components from git:
/etc/init.d/autohotspot:

# Make it executable
chmod +x autohotspot


Copy hostapd.service from git:
/usr/lib/systemd/system/hostapd.service

# unmask hostapd.service
systemctl unmask hostapd.service

#  Open firewall ports for dhcp/boot and DNS in the web admin

# Cop WiFi Scan web pages from git
/var/www/html/create_config.php
/var/www/html/scan_wifi.py
/var/www/html/logon.php

# modify apache to load the logon.php for android and apple online checks:

Edit /etc/apache2/sites-available/000-default.conf

# Add to <VirtualHost *:80> section

-----------------------------------
RewriteEngine On

# Redirect Apple devices for captive portal detection
RewriteRule ^/hotspot-detect.html$ /logon.php [L,R=302]

# Redirect Android devices for captive portal detection
RewriteRule ^/generate_204$ /logon.php [L,R=302]

# Redirect Windows devices for captive portal detection
RewriteRule ^/ncsi.txt$ /logon.php [L,R=302]

Symlink autohotspot.conf to the conf-enabled folder
------------------------------------



modify AllowOveride to All in /etc/apache2/apache2.conf:
---------------------------------------------------------
<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
</Directory>
---------------------------------------------------------


# Change frequency on boot base on /root/SA818.log file - copy files from git"
/root/SA818.log
/usr/local/sbin/set_on_boot.sh

# say ip script and supporting script - copy from git:
/usr/local/sbin/sayip.sh
/usr/local/sbin/speaktext.sh
