#!/bin/python3

import os
import platform

username = ''


# Make sure the script is being run as root
def check_root():
    if os.geteuid() != 0:
        print("Please run this script as root")
        exit()


# See if this script is running on RHEL/CentOS/Fedora/Rocky
def check_fedora():
    if platform.linux_distribution()[0] == 'Fedora' or platform.linux_distribution()[0] == 'Red Hat Enterprise Linux Server' or platform.linux_distribution()[0] == 'CentOS Linux' or platform.linux_distribution()[0] == 'Rocky Linux':
        return True
    else:
        return False


# See if this script is running on Ubuntu/Debian
def check_ubuntu():
    if platform.linux_distribution()[0] == 'Ubuntu' or platform.linux_distribution()[0] == 'Debian':
        return True
    else:
        return False


# Create a directory for Jellyfin
def create_jellyfin_dir():
    if not check_fedora() and check_ubuntu():
        os.system('wget -O- https://repo.jellyfin.org/install-debuntu.sh | sudo bash')
        os.system('systemctl enable jellyfin')
        os.system('systemctl start jellyfin')
    elif check_fedora() and not check_ubuntu():
        os.system('dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y')
        os.system('wget https://repo.jellyfin.org/releases/server/fedora/versions/stable/server/10.8.9/jellyfin-server-10.8.9-1.fc36.x86_64.rpm -O jellyfin.rpm')
        os.system('dnf localinstall jellyfin.rpm -y')
        os.system('rm -rf jellyfin.rpm')
        os.system('wget https://repo.jellyfin.org/releases/server/fedora/versions/stable/web/10.8.9/jellyfin-web-10.8.9-1.fc36.noarch.rpm -O jellyfin-web.rpm')
        os.system('dnf localinstall jellyfin-web.rpm -y')
        os.system('rm -rf jellyfin-web.rpm')
        os.system('wget https://repo.jellyfin.org/releases/server/centos/stable/server/jellyfin-server-10.8.9-1.el7.x86_64.rpm -O jellyfin.rpm')
        os.system('dnf localinstall jellyfin.rpm -y')
        os.system('rm -rf jellyfin.rpm')
        os.system('wget https://repo.jellyfin.org/releases/server/centos/stable/web/jellyfin-web-10.8.9-1.el7.noarch.rpm -O jellyfin-web.rpm')
        os.system('systemctl start jellyfin')
        os.system('systemctl enable jellyfin')
        os.system('firewall-cmd --add-service=jellyfin --permanent')
        os.system('firewall-cmd --reload')
        os.system('reboot now')
    else:
        print("This script only works on RHEL/CentOS/Fedora/Rocky or Ubuntu/Debian")
        exit()


# Main function
def main():
    check_root()
    create_jellyfin_dir()


if __name__ == '__main__':
    main()