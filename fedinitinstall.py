#!/bin/python3
import os

user = ""


def run_function(function_name):
    # Check if the function has already been run
    if os.path.isfile('function_log.txt'):
        with open('function_log.txt', 'r') as f:
            if function_name in f.read():
                print(f'{function_name} has already been run. Skipping...')
                return
    # Run the function
    globals()[function_name]()
    # Log the function
    with open('function_log.txt', 'a') as f:
        f.write(function_name + '\n')


# Install Necessary Groups
def install_groups():
    os.system(
        "dnf groupinstall -y 'Development Tools' 'Hardware Support' 'base-x' 'Fonts' 'Common NetworkManager Submodules' 'Printing Support' 'Input Methods' 'Multimedia' 'Development Libraries'")


# Install Necessary Packages
def install_packages():
    os.system("dnf -y install NetworkManager-config-connectivity-fedora bluedevil breeze-gtk breeze-icon-theme bzip2 "
              "cagibi colord-kde cups-pk-helper curl dhcp-server dolphin dkms gcc glibc-all-langpacks "
              "gnome-keyring-pam kcm_systemd kde-gtk-config kde-partitionmanager kde-print-manager "
              "kde-settings-pulseaudio kde-style-breeze kdegraphics-thumbnailers kdeplasma-addons kdialog kdnssd "
              "kernel-devel kf5-akonadi-server kf5-akonadi-server-mysql kf5-baloo-file kf5-kipi-plugins khotkeys "
              "kmenuedit konsole5 kscreen kscreenlocker ksshaskpass ksysguard kwalletmanager5 kwebkitpart kwin make "
              "pam-kwallet phonon-qt5-backend-gstreamer pinentry-qt plasma-breeze plasma-desktop plasma-desktop-doc "
              "plasma-drkonqi plasma-nm plasma-nm-l2tp plasma-nm-openconnect plasma-nm-openswan plasma-nm-openvpn "
              "plasma-nm-pptp plasma-nm-vpnc plasma-pa plasma-user-manager plasma-workspace "
              "plasma-workspace-geolocation polkit-kde qt5-qtbase-gui qt5-qtdeclarative sddm sddm-breeze sddm-kcm "
              "sni-qt xorg-x11-drv-libinput setroubleshoot kfind plasma-discover kfind firewall-config kgpg kate ark "
              "kget kcalc gwenview spectacle fedora-workstation-repositories dhcp-server usbutils util-linux-user "
              "pciutils htop wget zsh vim-enhanced jre NetworkManager NetworkManager-adsl NetworkManager-bluetooth "
              "NetworkManager-cloud-setup NetworkManager-config-connectivity-fedora NetworkManager-config-server "
              "NetworkManager-dispatcher-routing-rules NetworkManager-fortisslvpn NetworkManager-initscripts-ifcfg-rh "
              "NetworkManager-initscripts-updown NetworkManager-iodine NetworkManager-l2tp NetworkManager-libnm "
              "NetworkManager-libnm-devel NetworkManager-libreswan NetworkManager-openconnect NetworkManager-openvpn "
              "NetworkManager-ovs NetworkManager-ppp NetworkManager-pptp NetworkManager-ssh NetworkManager-sstp "
              "NetworkManager-strongswan NetworkManager-team NetworkManager-tui NetworkManager-vpnc "
              "NetworkManager-wifi NetworkManager-wwan cockpit-networkmanager kf5-networkmanager-qt "
              "kf5-networkmanager-qt kf5-networkmanager-qt-devel libproxy-networkmanager ModemManager NetworkManager-qt "
              "modem-manager-gui-cm-NetworkManager netplan-default-backend-NetworkManager python-networkmanager-doc "
              "python3-networkmanager libnma libnma-devel libnma-gtk4 libnma-gtk4-devel network-manager-applet "
              "nm-connection-editor shorewall-init.noarch strongswan-charon-nm zenmap nmap tcpdump xfsprogs "
              "wpa_supplicant vim-enhanced speedtest-cli remmina openvpn easy-rsa lrzsz python3-netifaces neofetch  "
              "python3-requests python3-libvirt libvirt kvm qemu-kvm virt-install virt-manager virt-viewer python3-dropbox "
              "strongswan avahi epel-release nextcloud-client python3-pip python3-pyOpenSSL python3-bs4 konsave ")


# Install PyPi Packages
def install_pip_packages():
    os.system("pip3 install --upgrade pip")
    os.system("pip3 install --upgrade setuptools")
    os.system("pip3 install --upgrade wheel")
    os.system("python -m pip install konsave")
    os.system("python -m pip install bs4")
    os.system("python -m pip install pyOpenSSL")


# Install Google Chrome
def install_chrome():
    os.system("dnf -y install fedora-workstation-repositories")
    os.system("dnf config-manager --set-enabled google-chrome")
    os.system("dnf -y install google-chrome-stable")


# Install Pycharm Professional
def install_pycharm():
    os.system("dnf -y copr enable haemka/pycharm-professional")
    os.system("dnf -y install pycharm-professional")
    os.system("wget -N https://download-cdn.jetbrains.com/toolbox/jetbrains-toolbox-1.27.2.13801.tar.gz -O /tmp/jetbrains-toolbox.tar.gz")
    os.system("tar -xzf /tmp/jetbrains-toolbox.tar.gz -C /opt/")
    os.system("chmod 777 -R /opt/*")


# Install Visual Studio Code
def install_vscode():
    os.system("dnf -y copr enable dani/vscode")
    os.system("dnf -y install code")


# Ask User if they want to set up a new user
def new_user():
    newuser = input("Would you like to set up a new user? [y/n]: ")
    if newuser == "y":
        new_username = input("Enter the username you would like to use: ")
        os.system("useradd -m -G wheel -s /bin/zsh " + new_username)
        os.system("passwd " + new_username)
        os.system("su - " + new_username)
    elif newuser == "n":
        print("Skipping user creation.")
    else:
        print("Invalid input. Skipping user creation.")


# Setup User Workspace Directory
def setup_workspace():
    global user
    user = input("Enter the username you would like to use: ")
    if not os.path.exists("/home/" + user):
        print("User does not exist. Skipping workspace setup.")
    else:
        os.system("mkdir /home/" + user + "/workspace")
        os.system("chown " + user + ":" + user + " /home/" + user + "/workspace")
        os.system("chmod 755 /home/" + user + "/workspace")


# Download files
def download_files():
    os.system("wget -N -O .zshrc https://www.dropbox.com/s/y6zleax42iow846/.zshrc?dl=1")
    os.system("wget -N -O .zshrc-root https://www.dropbox.com/s/afc0vm9dpde519c/.zshrc-root?dl=1"
              )
    os.system("wget -N -O nomachine_8.2.3_4_x86_64.rpm "
              "https://download.nomachine.com/download/8.2/Linux/nomachine_8.2.3_4_x86_64.rpm")
    os.system("wget -N -O Sweet-Ambar-Blue.tar.gz "
              "https://www.dropbox.com/s/ufs6iiajdv99s6x/Sweet-Ambar-Blue.tar.xz?dl=1")


# Install ZSH Config
def install_zsh():
    os.system("cp .zshrc /home/" + user + "/.zshrc")
    os.system("cp .zshrc-root /root/.zshrc")
    os.system("chsh -s /bin/zsh " + user)
    os.system("chsh -s /bin/zsh root")


# Install NoMachine
def install_nomachine():
    os.system("dnf -y localinstall ./nomachine_8.2.3_4_x86_64.rpm")


# KDE Theme install and Power Management/ScreenLocking Setup
def kde_setup():
    os.system("qdbus org.kde.PowerDevil /org/kde/PowerDevil/Behaviour "
              "org.kde.PowerDevil.Behaviour.SetScreenEnergySaving false")
    os.system("qdbus org.kde.screensaver /ScreenSaver org.freedesktop.ScreenSaver.SetActive false")
    os.system("qdbus org.kde.PowerDevil /org/kde/PowerDevil/Configuration "
              "org.kde.PowerDevil.Configuration.ScreenLock.SetTimeout 0")
    os.system("kde-install-theme --local Sweet-Ambar-Blue.tar.gz")
    os.system("kconfig_set kdeglobals General ColorScheme Sweet-Ambar-Blue PlasmaStyle Sweet-Ambar-Blue "
              "WindowDecoration Sweet-Ambar-Blue Icons candy-icons Cursors sweet-cursors SplashTheme Sweet-Ambar-Blue")


# Start SDDM and KDE
def start_sddm():
    os.system("systemctl enable sddm")
    os.system("systemctl start sddm")
    os.system("systemctl set-default graphical.target")


# Create USBEthernet NetworkManager Connection
def create_usbethernet_connection():
    os.system('/etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "[connection]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "id=USBethernet" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system(
        'echo "uuid=aa92cd5a-296b-3392-b500-2272a787d5c5" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "type=ethernet" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "autoconnect-priority=-100" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "zone=internal" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "[ethernet]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "mac-address=A0:CE:C8:03:D4:62" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "[ipv4]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "method=manual" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "addresses1=192.168.111.1/24" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "method=manual" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "[ipv6]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "method=disabled" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('echo "[proxy]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet')
    os.system('systemctl restart NetworkManager')


# Setup  Avahi/mDNS
def avahi_setup():
    os.system("firewall-cmd --permanent --add-service=mdns")
    os.system("firewall-cmd --reload")
    # Get hostname from hostnamectl
    hostname = os.popen("hostnamectl | grep hostname | awk '{print $3}'").read()
    # Set hostname in avahi-daemon.conf
    os.system("sed -i 's/.*host-name=.*/host-name=" + hostname + "/' /etc/avahi/avahi-daemon.conf")
    os.system("systemctl enable avahi-daemon")
    os.system("systemctl start avahi-daemon")


# Ask User how they want to set up Fedora
def fed_type():
    # Get hostname from hostnamectl
    hostname = os.popen("hostnamectl | grep hostname | awk '{print $3}'").read()
    if "fedorabox" in hostname:
        os.system("wget -N -O fedboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedboxmotd.txt")
        os.system("echo fedboxmotd.txt >> /etc/motd")
        os.system("python3 fedorabox.py")
    elif "hal9001" in hostname:
        os.system("wget -N -O hal9001motd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedhal9k1motd.txt")
        os.system("echo hal9001motd.txt >> /etc/motd")
        os.system("python3 hal9001.py")
    elif "laptop" in hostname:
        os.system("wget -N -O laptopmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedlaptopmotd.txt")
        os.system("echo laptopmotd.txt >> /etc/motd")
        os.system("python3 laptop.py")
    elif "router" in hostname:
        os.system("wget -N -O routermotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedroutermotd.txt")
        os.system("echo routermotd.txt >> /etc/motd")
        os.system("python3 router.py")
    elif "shitbox" in hostname:
        os.system("wget --no-check-check-certificate -N -O shitboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/shitboxmotd.txt")
        os.system("echo shitboxmotd.txt >> /etc/motd")
        os.system("python3 shitbox.py")
    else:
        print("Invalid Input")


# Main Function
def main():
    run_function("install_groups")
    run_function("install_packages")
    run_function("install_pip_packages")
    run_function("install_chrome")
    run_function("install_pycharm")
    run_function("install_vscode")
    run_function("new_user")
    run_function("setup_workspace")
    run_function("download_files")
    run_function("install_zsh")
    run_function("start_sddm")
    run_function("kde_setup")
    run_function("install_nomachine")
    run_function("create_usbethernet_connection")
    run_function("fed_type")


if __name__ == '__main__':
    main()
