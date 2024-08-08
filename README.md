Start with asl3 pi image

run raspi-config and set the wifi region to US

# Install some things:
sudo apt-get install hostapd dnsmasq telnet traceroute git php libapache2-mod-php openvpn

# Set openvpn to start at boot:
systemctl enable openvpn-client@client

# Copy web files from git:
cp ASL3-Mods/var/www/html/* /var/www/html

/var/www/html/vpn.html
/var/www/html/upload.php
/var/www/html/create_config.php
/var/www/html/scan_wifi.py
/var/www/html/logon.php

# change group of /etc/openvpn/client to www-data and add write permission to group
chown root:www-data /etc/openvpn/client
chmod g+w /etc/openvpn/client

# Allow www-data to access network devices:
usermod -aG netdev www-data

# add to sudo using visudo:
www-data ALL=(ALL) NOPASSWD: /sbin/iwlist
www-data ALL=(ALL) NOPASSWD: /usr/bin/nmcli
www-data ALL=(ALL) NOPASSWD: /usr/sbin/reboot



# Copy and make executable autoAP script from git:
cp ASL3-Mods/usr/local/bin/start_hostap.sh /usr/local/bin/
chmod +x start_hostap.sh

# Copy and make executable AutoAP components from git:
cp ASL3-Mods/etc/init.d/autohotspot /etc/init.d/
chmod +x /etc/init.d/autohotspot


Copy hostapd.service from git:
/usr/lib/systemd/system/hostapd.service

# unmask and disable hostapd.service
systemctl unmask hostapd.service

systemctl disable hostapd.service

# copy dnsmasq.conf from git
cp ASL3-Mods/etc/dnsmasq.conf /etc/cd /et        

# Open firewall ports for dhcp and DNS in the web admin

# modify apache to load the logon.php for android and apple online checks:

# Edit /etc/apache2/sites-available/000-default.conf

Add to <VirtualHost *:80> section

-----------------------------------

RewriteEngine On

# Redirect Apple devices for captive portal detection
RewriteRule ^/hotspot-detect.html$ /logon.php [L,R=302]

# Redirect Android devices for captive portal detection
RewriteRule ^/generate_204$ /logon.php [L,R=302]

# Redirect Windows devices for captive portal detection
RewriteRule ^/ncsi.txt$ /logon.php [L,R=302]

-----------------------------------



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


# copy sbin files from git:
cp ASL3-Mods/usr/local/sbin/* /usr/local/sbin/

/usr/local/sbin/set_on_boot.sh
/usr/local/sbin/sayip.sh
/usr/local/sbin/speaktext.sh

# Make them executable:
chmod +x sayip.sh
chmod +x set_on_boot.sh
chmod +x speaktext.sh

# add the following to rc.local:

/usr/local/bin/start_hostapd.sh

/usr/local/sbin/set_on_boot.sh

# Enable RX LED
in rpt.conf:

[events]
cop,62,GPIO4:1 = c|t|RPT_RXKEYED
cop,62,GPIO4:0 = c|f|RPT_RXKEYED



