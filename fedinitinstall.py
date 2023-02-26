#!/bin/python3
import os
import subprocess

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
    try:
        os.system("dnf config-manager --add-repo https://download.opensuse.org/repositories/shells:zsh-users:zsh-completions/Fedora_36/shells:zsh-users:zsh-completions.repo")
    except os.error as e:
        print(e)

# Install network packages
def install_network_packages():
    try:
        os.system("dnf -y install NetworkManager-config-connectivity-fedora plasma-nm plasma-nm-l2tp plasma-nm-openconnect plasma-nm-openswan plasma-nm-openvpn plasma-nm-pptp plasma-nm-vpnc NetworkManager NetworkManager-adsl NetworkManager-bluetooth NetworkManager-config-connectivity-fedora NetworkManager-config-server NetworkManager-dispatcher-routing-rules NetworkManager-fortisslvpn NetworkManager-l2tp NetworkManager-libnm NetworkManager-libnm-devel NetworkManager-libreswan NetworkManager-openconnect NetworkManager-openvpn NetworkManager-ovs NetworkManager-ppp NetworkManager-pptp NetworkManager-ssh NetworkManager-sstp NetworkManager-strongswan NetworkManager-vpnc NetworkManager-wifi NetworkManager-wwan kf5-networkmanager-qt kf5-networkmanager-qt-devel libproxy-networkmanager ModemManager modem-manager-gui-cm-NetworkManager python3-networkmanager network-manager-applet nm-connection-editor wpa_supplicant openvpn easy-rsa strongswan avahi aircrack-ng bind bind-utils rsync")
    except os.error as e:
        print(e)

    try:
        os.system(
            "dnf -y install util-linux-user python3-requests python3-libvirt libvirt bridge-utils python3-dropbox vim-enhanced speedtest-cli remmina lrzsz python3-netifaces neofetch nmap tcpdump xfsprogs kmousetool libnma libnma-devel libnma-gtk4 libnma-gtk4-devel tar xz unzip zip pciutils htop wget zsh jre plasma-pk-updates kget kcalc gwenview spectacle fedora-workstation-repositories dhcp-server usbutils util-linux-user sni-qt xorg-x11-drv-libinput setroubleshoot kfind plasma-discover kfind firewall-config kgpg kate ark plasma-drkonqi bluedevil breeze-gtk breeze-icon-theme bzip2 zsh-completions lsb cagibi colord-kde cups-pk-helper curl dhcp-server dolphin dkms gcc glibc-all-langpacks python3-netifaces gnome-keyring-pam kcm_systemd kde-gtk-config kde-partitionmanager kde-print-manager python3-psutil kde-settings-pulseaudio kde-style-breeze kdegraphics-thumbnailers kdeplasma-addons kdialog kdnssd kernel-devel kf5-akonadi-server kf5-akonadi-server-mysql kf5-baloo-file kf5-kipi-plugins khotkeys kmenuedit konsole5 kscreen kscreenlocker ksshaskpass ksysguard kwalletmanager5 kwebkitpart kwin make pam-kwallet phonon-qt5-backend-gstreamer pinentry-qt plasma-breeze plasma-desktop plasma-desktop-doc plasma-workspace-geolocation polkit-kde qt5-qtbase-gui qt5-qtdeclarative sddm sddm-breeze sddm-kcm plasma-pa plasma-user-manager plasma-workspace net-tools dnf-plugins-core iperf3 sshpass mlocate vnstat lm_sensors mtd-utils kf5-kconfig kf5-kconfig-core kf5-kconfig-devel kf5-kconfig-gui kf5-kconfig-doc kcharselect nextcloud-client python3-pip python3-pyOpenSSL python3-beautifulsoup4 python3-psutil")
    except os.error as e:
        print(e)

# Install PyPi Packages
def install_pip_packages():
    os.system("pip3 install --upgrade pip")
    os.system("pip3 install --upgrade wheel")
    os.system("python -m pip install konsave")
    os.system("python -m pip install bs4")
    os.system("python -m pip install pyOpenSSL")


# Configure applications
def configure_applications():
    os.system("sensors-detect --auto")


# Install Google Chrome
def install_chrome():
    os.system("dnf -y install fedora-workstation-repositories")
    os.system("dnf config-manager --set-enabled google-chrome")
    os.system("dnf -y install google-chrome-stable")


# Install Pycharm Professional
def install_pycharm():
    os.system(
        "wget https://download-cdn.jetbrains.com/toolbox/jetbrains-toolbox-1.27.2.13801.tar.gz -O /tmp/jetbrains-toolbox.tar.gz")
    os.system("tar -xzf /tmp/jetbrains-toolbox.tar.gz -C /opt/")
    os.system("chmod 777 -R /opt/*")
    # Run Pycharm Professional Installer from Jetbrains Toolbox
    os.system("/opt/jetbrains-toolbox-1.27.2.13801/jetbrains-toolbox --install-pycharm-professional")
    os.system("sleep 30")
    os.system("/opt/jetbrains-toolbox-1.27.2.13801/jetbrains-toolbox --install-clion")
    os.system("sleep 30")
    os.system("/opt/jetbrains-toolbox-1.27.2.13801/jetbrains-toolbox --install-phpstorm")
    os.system("sleep 30")
    os.system("/opt/jetbrains-toolbox-1.27.2.13801/jetbrains-toolbox --install-webstorm")
    os.system("sleep 30")
    os.system("/opt/jetbrains-toolbox-1.27.2.13801/jetbrains-toolbox --install-android-studio")
    os.system("sleep 30")


# Install Visual Studio Code
def install_vscode():
    os.system("rpm --import https://packages.microsoft.com/keys/microsoft.asc")
    command = "echo -e '[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/vscode.repo"
    os.system(command)
    os.system("dnf -y check-update")
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
    hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout
    user = input("Enter the username you would like to use: ")
    os.environ["user"] = user
    if not os.path.exists("/home/" + user):
        print("User does not exist. Skipping workspace setup.")
    else:
        os.system("mkdir /home/{}/Desktop".format(user))
        os.system("mkdir /home/{}/Desktop/workspace".format(user))
        os.system("mkdir /home/{}/Desktop/workspace/Scripts".format(user))
        os.system("mkdir /home/{}/Desktop/workspace/{}config".format(user, hostname))
        os.system("mkdir /home/{}/Desktop/workspace/{}config/logs".format(user, hostname))
        os.system("mkdir /home/{}/Desktop/workspace/{}config/installscripts".format(user, hostname))
        # Copy Scripts to User Workspace/Scripts
        os.system("cp -air *.sh *.py /home/{}/Desktop/workspace/Scripts".format(user))


# Download files
def download_files():
    os.system("wget -O .zshrc https://www.dropbox.com/s/y6zleax42iow846/.zshrc?dl=1")
    os.system("wget -O .zshrc-root https://www.dropbox.com/s/afc0vm9dpde519c/.zshrc-root?dl=1"
              )
    os.system("wget -O nomachine_8.2.3_4_x86_64.rpm "
              "https://download.nomachine.com/download/8.2/Linux/nomachine_8.2.3_4_x86_64.rpm")


# Install ZSH Config
def install_zsh():
    os.system("cp .zshrc /home/" + user + "/.zshrc")
    os.system("cp .zshrc-root /root/.zshrc")
    os.system("chsh -s /bin/zsh " + user)
    os.system("chsh -s /bin/zsh root")


# Install NoMachine
def install_nomachine():
    os.system("mv nomachine*.rpm nomachine.rpm")
    os.system("dnf -y localinstall ./nomachine.rpm")


# Start SDDM and KDE
def start_sddm():
    os.system("systemctl enable sddm")
    os.system("systemctl set-default graphical.target")
    os.system("systemctl start sddm")


# Create USBEthernet NetworkManager Connection
def create_usbethernet_connection():
    os.system('touch /etc/NetworkManager/system-connections/ifcfg-USBethernet')
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
    hostname = subprocess.run(["hostnamectl", "status"], capture_output=True, text=True).stdout.splitlines()[1].split()[1]
    # Delete avahi_daemon.conf
    os.system("rm /etc/avahi/avahi-daemon.conf -rf")
    # Create avahi_daemon.conf
    os.system("touch /etc/avahi/avahi-daemon.conf")
    os.system('echo "[server]" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "host-name=' + hostname + '" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "use-ipv4=yes" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "use-ipv6=yes" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "allow-interfaces=" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "ratelimit-interval-usec=1000000" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "ratelimit-burst=1000" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo /n >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "[wide-area]" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "enable-wide-area=yes" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo /n >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "[publish]" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "publish-hinfo=no" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "publish-workstation=no" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo /n >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "[rlimits]" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "rlimit-core=0" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "rlimit-data=4194304" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "rlimit-fsize=0" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "rlimit-nofile=768" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "rlimit-stack=4194304" >> /etc/avahi/avahi-daemon.conf')
    os.system('echo "rlimit-nproc=3" >> /etc/avahi/avahi-daemon.conf')
    os.system('systemctl enable avahi-daemon')
    os.system('systemctl start avahi-daemon')


def kde_setup():
    # Turn off Energy Saving> Screen Energy Saving
    os.system("kwriteconfig5 --file kscreenlockerrc --group Daemon --key Autolock false".format(user))
    # Set Button Events Handling> When Power Button is Pressed to Shutdown
    os.system("kwriteconfig5 --file powermanagementprofilesrc --group General --key ButtonPower 'shutdown'".format(user))
    # Set Screen Locking> Lock Screen Automatically to Never
    os.system("kwriteconfig5 --file powermanagementprofilesrc --group General --key LockScreen false".format(user))


# Setup VNStat
def vnstat_setup():
    interfaces = subprocess.run(["nmcli", "device", "status"], capture_output=True, text=True).stdout.splitlines()
    for interface in interfaces:
        os.system("vnstat -u -i " + interface.split()[0])
    os.system("systemctl enable vnstat")
    os.system("systemctl start vnstat")



# Ask User how they want to set up Fedora
def fed_type():
    # Get hostname from hostnamectl
    hostname = os.popen("hostnamectl | grep hostname | awk '{print $3}'").read()
    if "fedorabox" in hostname:
        os.system("wget -O fedboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedboxmotd.txt")
        os.system("echo fedboxmotd.txt >> /etc/motd")
    elif "hal9001" in hostname:
        os.system("wget -O hal9001motd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedhal9k1motd.txt")
        os.system("echo hal9001motd.txt >> /etc/motd")
    elif "laptop" in hostname:
        os.system("wget -O laptopmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedlaptopmotd.txt")
        os.system("echo laptopmotd.txt >> /etc/motd")
    elif "router" in hostname:
        os.system("wget -O routermotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedroutermotd.txt")
        os.system("echo routermotd.txt >> /etc/motd")
    elif "shitbox" in hostname:
        os.system("wget -O shitboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/shitboxmotd.txt")
        os.system("echo shitboxmotd.txt >> /etc/motd")
    else:
        print("Invalid Input")


# Main Function
def main():
    run_function("install_groups")
    run_function("install_packages")
    run_function("install_network_packages")
    run_function("install_pip_packages")
    run_function("configure_applications")
    run_function("install_chrome")
    run_function("install_pycharm")
    run_function("install_vscode")
    run_function("new_user")
    run_function("setup_workspace")
    run_function("download_files")
    run_function("install_zsh")
    run_function("start_sddm")
    run_function("install_nomachine")
    run_function("create_usbethernet_connection")
    run_function("avahi_setup")
    run_function("vnstat_setup")
    run_function("kde_setup")
    run_function("fed_type")


if __name__ == '__main__':
    main()
