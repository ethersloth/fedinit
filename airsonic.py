#!/bin/python3

import os
import platform


# Check if running as root
def check_root():
    if os.getuid() != 0:
        print('Please run as root')
        exit()


# Check if running on Ubuntu/Debian
def check_ubuntu():
    if platform.linux_distribution()[0] == 'Ubuntu' or platform.linux_distribution()[0] == 'Debian':
        return True
    else:
        return False


# Check if running on Fedora/RHEL/CentOS/Rocky
def check_fedora():
    if platform.linux_distribution()[0] == 'Fedora' or platform.linux_distribution()[0] == 'Red Hat Enterprise Linux Server' or platform.linux_distribution()[0] == 'CentOS Linux' or platform.linux_distribution()[0] == 'Rocky Linux':
        return True
    else:
        return False


# Ubuntu/Debian Commands
def ubuntu():
    os.system('apt -y install openjdk-8-jre')
    os.system('update-alternatives --config java')


# Fedora/RHEL/CentOS/Rocky Commands
def fedora():
    os.system('yum -y install java')
    os.system('yum install java-devel')
    os.system('alternatives --config java')


# Download Airsonic.war package
def download():
    os.system('wget --no-check-certificate -N https://objects.githubusercontent.com/github-production-release-asset-2e65be/221316636/f0f253d0-24f9-40cb-bef0-3a9895dc5324?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230204%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230204T184634Z&X-Amz-Expires=300&X-Amz-Signature=cc7fa0d412bd2ed082ae228a2fce0de10724c01292536a47ddbd6288fd7136f5&X-Amz-SignedHeaders=host&actor_id=41842231&key_id=0&repo_id=221316636&response-content-disposition=attachment%3B%20filename%3Dairsonic.war&response-content-type=application%2Foctet-stream -O airsonic.war')
    os.system('useradd airsonic')
    os.system('mkdir /var/airsonic')
    os.system('chown -R airsonic:airsonic /var/airsonic')
    os.system('cp -air airsonic.war /var/airsonic')
    os.system('chown -R airsonic:airsonic /var/airsonic')
    os.system('wget https://raw.githubusercontent.com/airsonic/airsonic/master/contrib/airsonic.service -O /etc/systemd/system/airsonic.service')
    os.system('systemctl daemon-reload')
    os.system('systemctl enable airsonic')
    os.system('systemctl start airsonic')
    if not check_ubuntu() and check_fedora():
        os.system('wget https://raw.githubusercontent.com/airsonic/airsonic/master/contrib/airsonic-systemd-env -O /etc/sysconfig/airsonic')
        os.system('systemctl daemon-reload')
        os.system('firewall-cmd --zone=external --add-port=8080/tcp --permanent')
        os.system('firewall-cmd --reload')
        os.system('systemctl restart airsonic')
    elif check_ubuntu() and not check_fedora():
        os.system('wget https://raw.githubusercontent.com/airsonic/airsonic/master/contrib/airsonic-ubuntu -O /etc/default/airsonic')
        os.system('systemctl daemon-reload')
        os.system('systemctl enable airsonic.service')
        os.system('systemctl start airsonic.service')
        os.system('ufw allow 8080/tcp')
        os.system('systemctl restart airsonic')


# Main
def main():
    ubuntu()
    fedora()
    download()


# Run
if __name__ == '__main__':
    check_root()
    main()
