#!/bin/python3
import os
import subprocess

import dropbox

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


# Add Repos
def add_repos():
    repos = ["https://download.opensuse.org/repositories/shells:zsh-users:zsh-completions/Fedora_36/shells:zsh-users:zsh-completions.repo"]
    for repo in repos:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("dnf config-manager --add-repo {} >> output.log 2>&1".format(repo + '\n'))
            # Write repo to repo install log file
            os.system("touch repo_install_log.txt >> output.log 2>&1")
            log_file.close()
            with open('repo_install_log.txt', 'a') as f:
                f.write(repo + '\n')
                f.close()
        except os.error:
            print("Error adding repo: {}".format(repo + '\n'))
            print("Continuing with installation...")
            continue


# Install Necessary Groups
def install_groups():
    groups = ["Development Tools",
                "Hardware Support",
                "base-x",
                "Fonts",
                "Common NetworkManager Submodules",
                "Printing Support",
                "Input Methods",
                "Multimedia",
                "Development Libraries"]

    # Install the packages
    for group in groups:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("dnf groupinstall -y '{}' >> output.log 2>&1".format(group + '\n'))
            # Write repo to repo install log file
            os.system("touch group_install_log.txt >> output.log 2>&1")
            log_file.close()
            with open('group_install_log.txt', 'a') as f:
                f.write(group + '\n')
                f.close()
        except os.error:
            print("Error installing group: {}".format(group + '\n'))
            print("Continuing with installation...")
            continue

# Install Necessary Packages
def install_packages():
    packages = ["util-linux-user",
                "python3-requests",
                "python3-libvirt",
                "libvirt",
                "bridge-utils",
                "python3-dropbox",
                "vim-enhanced",
                "speedtest-cli",
                "remmina",
                "lrzsz",
                "python3-netifaces",
                "neofetch",
                "nmap",
                "tcpdump",
                "xfsprogs",
                "kmousetool",
                "libnma",
                "libnma-devel",
                "libnma-gtk4",
                "libnma-gtk4-devel",
                "tar",
                "xz",
                "unzip",
                "zip",
                "pciutils",
                "htop",
                "wget",
                "zsh",
                "jre",
                "plasma-pk-updates",
                "kget",
                "kcalc",
                "gwenview",
                "spectacle",
                "fedora-workstation-repositories",
                "dhcp-server",
                "usbutils",
                "util-linux-user",
                "sni-qt",
                "xorg-x11-drv-libinput",
                "setroubleshoot",
                "kfind",
                "plasma-discover",
                "kfind",
                "firewall-config",
                "kgpg",
                "kate",
                "ark",
                "plasma-drkonqi",
                "bluedevil",
                "breeze-gtk",
                "breeze-icon-theme",
                "bzip2",
                "zsh-completions",
                "lsb",
                "cagibi",
                "colord-kde",
                "cups-pk-helper",
                "curl",
                "dolphin",
                "dkms",
                "gcc",
                "glibc-all-langpacks",
                "python3-netifaces",
                "gnome-keyring-pam",
                "kcm_systemd",
                "kde-gtk-config",
                "kde-partitionmanager",
                "kde-print-manager",
                "python3-psutil",
                "kde-settings-pulseaudio",
                "kde-style-breeze",
                "kdegraphics-thumbnailers",
                "kdeplasma-addons",
                "kdialog",
                "kdnssd",
                "kernel-devel",
                "kf5-akonadi-server",
                "kf5-akonadi-server-mysql",
                "kf5-baloo-file",
                "kf5-kipi-plugins",
                "khotkeys",
                "kmenuedit",
                "konsole5",
                "kscreen",
                "kscreenlocker",
                "ksshaskpass",
                "ksysguard",
                "kwalletmanager5",
                "kwebkitpart",
                "kwin",
                "make",
                "pam-kwallet",
                "phonon-qt5-backend-gstreamer",
                "pinentry-qt",
                "plasma-breeze",
                "plasma-desktop",
                "plasma-desktop-doc",
                "plasma-workspace-geolocation",
                "polkit-kde",
                "qt5-qtbase-gui",
                "qt5-qtdeclarative",
                "sddm",
                "sddm-breeze",
                "sddm-kcm",
                "plasma-pa",
                "plasma-user-manager",
                "plasma-workspace",
                "net-tools",
                "dnf-plugins-core",
                "iperf3",
                "sshpass",
                "mlocate",
                "vnstat",
                "lm_sensors",
                "mtd-utils",
                "kf5-kconfig",
                "kf5-kconfig-core",
                "kf5-kconfig-devel",
                "kf5-kconfig-gui",
                "kf5-kconfig-doc",
                "kcharselect",
                "nextcloud-client",
                "python3-pip",
                "python3-pyOpenSSL",
                "python3-beautifulsoup4",
                "python3-psutil",
                "python3-pip",
                "barrier",
    ]

    for package in packages:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("dnf install -y {} >> output.log 2>&1".format(package))
            # Write packages to package install log file
            os.system("touch package_install_log.txt >> output.log 2>&1")
            log_file.close()
            with open('package_install_log.txt', 'a') as f:
                f.write(package + '\n')
                f.close()
        except os.error:
            print("Error installing package: {}".format(package))
            print("Continuing with installation...")
            return

# Install network packages
def install_network_packages():
    network_packages = ["NetworkManager-config-connectivity-fedora",
                        "plasma-nm plasma-nm-l2tp",
                        "plasma-nm-openconnect",
                        "plasma-nm-openswan",
                        "plasma-nm-openvpn",
                        "plasma-nm-pptp",
                        "plasma-nm-vpnc",
                        "NetworkManager",
                        "NetworkManager-adsl",
                        "NetworkManager-bluetooth",
                        "NetworkManager-config-server",
                        "NetworkManager-dispatcher-routing-rules",
                        "NetworkManager-fortisslvpn",
                        "NetworkManager-l2tp",
                        "NetworkManager-libnm",
                        "NetworkManager-libnm-devel",
                        "NetworkManager-libreswan",
                        "NetworkManager-openconnect",
                        "NetworkManager-openvpn",
                        "NetworkManager-ovs",
                        "NetworkManager-ppp",
                        "NetworkManager-pptp",
                        "NetworkManager-ssh",
                        "NetworkManager-sstp",
                        "NetworkManager-strongswan",
                        "NetworkManager-vpnc",
                        "NetworkManager-wifi",
                        "NetworkManager-wwan",
                        "kf5-networkmanager-qt",
                        "kf5-networkmanager-qt-devel",
                        "libproxy-networkmanager",
                        "ModemManager",
                        "modem-manager-gui-cm-NetworkManager",
                        "python3-networkmanager",
                        "network-manager-applet",
                        "nm-connection-editor",
                        "wpa_supplicant",
                        "openvpn",
                        "easy-rsa",
                        "strongswan",
                        "avahi",
                        "aircrack-ng",
                        "bind",
                        "bind-utils",
                        "rsync",
                        "nmap",
                        "wireshark"
                        ]
    for package in network_packages:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("dnf install -y {} >> output.log 2>&1".format(package))
            # Write packages to package install log file
            os.system("touch package_install_log.txt >> output.log 2>&1")
            log_file.close()
            with open('package_install_log.txt', 'a') as f:
                f.write(package + '\n')
                f.close()
        except os.error:
            print("Error installing package: {}".format(package))
            print("Continuing with installation...")
            return

# Install PyPi Packages
def install_pip_packages():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("pip3 install --upgrade pip >> output.log 2>&1")
    os.system("pip3 install --upgrade wheel >> output.log 2>&1")
    log_file.close()
    pip_packages = ["konsave", "bs4", "pyOpenSSL"]
    for package in pip_packages:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("pip3 install {} >> output.log 2>&1".format(package + '\n'))
            # Write package to package install log file
            os.system("touch package_install_log.txt >> output.log 2>&1")
            log_file.close()
            with open('package_install_log.txt', 'a') as f:
                f.write(package + '\n')
                f.close()
        except os.error:
            print("Error installing package: {}".format(package + '\n'))
            print("Continuing with installation...")
            continue


# Configure applications
def configure_applications():
    # Open a file for logging
    log_file = open("output.log", "w")
    conf_app_commands = ["sensors-detect --auto >> output.log 2>&1"]
    log_file.close()
    for conf_app_command in conf_app_commands:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system(conf_app_command + '\n')
            # Write conf_app_command to conf_app_command log file
            os.system("touch conf_app_command_log.txt >> output.log 2>&1")
            log_file.close()
            with open('conf_app_command_log.txt', 'a') as f:
                f.write(conf_app_command + '\n')
                f.close()
        except os.error:
            print("Error configuring application: {}".format(conf_app_command + '\n'))
            print("Continuing with installation...")
            continue


# Install Google Chrome
def install_chrome():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("dnf -y install fedora-workstation-repositories >> output.log 2>&1")
    os.system("dnf config-manager --set-enabled google-chrome >> output.log 2>&1")
    os.system("dnf -y install google-chrome-stable >> output.log 2>&1")
    log_file.close()


# Install Visual Studio Code
def install_vscode():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("rpm --import https://packages.microsoft.com/keys/microsoft.asc >> output.log 2>&1")
    command = "echo -e '[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/vscode.repo >> output.log 2>&1"
    os.system(command)
    os.system("dnf -y check-update >> output.log 2>&1")
    os.system("dnf -y install code  >> output.log 2>&1")
    log_file.close()


# Ask User if they want to set up a new user
def new_user():
    newuser = input("Would you like to set up a new user? [y/n]: ")
    if newuser == "y":
        # Open a file for logging
        log_file = open("output.log", "w")
        new_username = input("Enter the username you would like to use: ")
        os.system("useradd -m -G wheel -s /bin/zsh " + new_username + " >> output.log 2>&1")
        os.system("passwd " + new_username + " >> output.log 2>&1")
        os.system("su - " + new_username + " >> output.log 2>&1")
        log_file.close()
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
        # Open a file for logging
        log_file = open("output.log", "w")
        os.system("mkdir /home/{}/Desktop >> output.log 2>&1".format(user))
        os.system("mkdir /home/{}/Desktop/workspace >> output.log 2>&1".format(user))
        os.system("mkdir /home/{}/Desktop/workspace/Scripts >> output.log 2>&1".format(user))
        os.system("mkdir /home/{}/Desktop/workspace/{}config >> output.log 2>&1".format(user, hostname))
        os.system("mkdir /home/{}/Desktop/workspace/{}config/logs >> output.log 2>&1".format(user, hostname))
        os.system("mkdir /home/{}/Desktop/workspace/{}config/installscripts >> output.log 2>&1".format(user, hostname))
        # Copy Scripts to User Workspace/Scripts
        os.system("cp -air *.sh *.py /home/{}/Desktop/workspace/Scripts >> output.log 2>&1".format(user))
        os.system("chown -R {}:{} /home/{}/ >> output.log 2>&1".format(user, user, user))
        log_file.close()


# Install Pycharm Professional
def install_pycharm():
    # Open a file for logging
    log_file = open("output.log", "w")
    # Download Pycharm
    os.system('wget -O jetbrains-toolbox.tar.gz --cut-dirs=2 -A "*.tar.gz" "https://download-cdn.jetbrains.com/toolbox/jetbrains-toolbox-*.tar.gz' + '" >> output.log 2>&1')
    # Extract Pycharm
    os.system("tar -xvf jetbrains-toolbox.tar.gz >> output.log 2>&1")
    # Install Pycharm
    os.system("./jetbrains-toolbox-*/jetbrains-toolbox >> output.log 2>&1")

    # Install Pycharm Professional
    os.system('wget -O pycharm-professional.tar.gz --cut-dirs=2 -A "*.tar.gz" "https://download-cdn.jetbrains.com/python/pycharm-professional-*.tar.gz" >> output.log 2>&1')
    os.system("tar -xvf pycharm-professional.tar.gz >> output.log 2>&1")
    os.system("mv pycharm-* /opt/pycharm-professional >> output.log 2>&1")
    os.system("ln -s /opt/pycharm-professional/bin/pycharm.sh /usr/local/bin/pycharm >> output.log 2>&1")
    log_file.close()


# Download files
def download_files():
    os.system("wget -O .zshrc https://www.dropbox.com/s/y6zleax42iow846/.zshrc?dl=1")
    os.system("wget -O .zshrc-root https://www.dropbox.com/s/afc0vm9dpde519c/.zshrc-root?dl=1")


# Download and Install NoMachine
def download_nomachine():
    # Open a file for logging
    os.system("wget -O nomachine.rpm --cut-dirs=2 -A '*x86_64.rpm' 'https://download.nomachine.com/download/*/Linux/nomachine_*_x86_64.rpm'")
    os.system("dnf -y install nomachine.rpm >> output.log 2>&1")



# Install ZSH Config
def install_zsh():
    global user
    os.system("cp .zshrc /home/{}/.zshrc >> output.log 2>&1".format(user))
    os.system("cp .zshrc-root /root/.zshrc >> output.log 2>&1")
    # Change ownership of /home/{user}
    os.system("chown -R {}:{} /home/{}/".format(user, user, user))
    os.system("chsh -s /bin/zsh {} ".format(user))
    os.system("chsh -s /bin/zsh root")



# Start SDDM and KDE
def start_sddm():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("systemctl enable sddm >> output.log 2>&1")
    os.system("systemctl set-default graphical.target >> output.log 2>&1")
    os.system("systemctl start sddm >> output.log 2>&1")
    log_file.close()


# Create USBEthernet NetworkManager Connection
def create_usbethernet_connection():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system('touch /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "[connection]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "id=USBethernet" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system(
        'echo "uuid=aa92cd5a-296b-3392-b500-2272a787d5c5" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "type=ethernet" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "autoconnect-priority=-100" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "zone=internal" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "[ethernet]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "mac-address=A0:CE:C8:03:D4:62" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "[ipv4]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "method=manual" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "addresses1=192.168.111.1/24" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "method=manual" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "[ipv6]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "method=disabled" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('echo "[proxy]" >> /etc/NetworkManager/system-connections/ifcfg-USBethernet >> output.log 2>&1')
    os.system('systemctl restart NetworkManager >> output.log 2>&1')
    log_file.close()


# Setup  Avahi/mDNS
def avahi_setup():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("firewall-cmd --permanent --add-service=mdns >> output.log 2>&1")
    os.system("firewall-cmd --reload >> output.log 2>&1")
    # Get hostname from hostnamectl
    hostname = subprocess.run(["hostnamectl", "status"], capture_output=True, text=True).stdout.splitlines()[1].split()[1]
    # Delete avahi_daemon.conf
    os.system("rm /etc/avahi/avahi-daemon.conf -rf >> output.log 2>&1")
    # Create avahi_daemon.conf
    os.system("touch /etc/avahi/avahi-daemon.conf >> output.log 2>&1")
    os.system('echo "[server]" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "host-name=' + hostname + '" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "use-ipv4=yes" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "use-ipv6=yes" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "allow-interfaces=" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "ratelimit-interval-usec=1000000" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "ratelimit-burst=1000" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo /n >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "[wide-area]" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "enable-wide-area=yes" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo /n >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "[publish]" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "publish-hinfo=no" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "publish-workstation=no" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo /n >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "[rlimits]" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "rlimit-core=0" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "rlimit-data=4194304" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "rlimit-fsize=0" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "rlimit-nofile=768" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "rlimit-stack=4194304" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('echo "rlimit-nproc=3" >> /etc/avahi/avahi-daemon.conf >> output.log 2>&1')
    os.system('systemctl enable avahi-daemon >> output.log 2>&1')
    os.system('systemctl start avahi-daemon >> output.log 2>&1')
    log_file.close()


def kde_setup():
    # Turn off Energy Saving> Screen Energy Saving
    kde_setup_commands = ["kwriteconfig5 --file kscreenlockerrc --group Daemon --key Autolock false",
                          "kwriteconfig5 --file powermanagementprofilesrc --group General --key ButtonPower 'shutdown'",
                          "kwriteconfig5 --file powermanagementprofilesrc --group General --key LockScreen false"]
    try:
        for kde_setup_command in kde_setup_commands:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system(kde_setup_command + " >> output.log 2>&1".format(user))
            # write kde_setup_command to log file
            os.system("touch kde_setup_command.log >> output.log 2>&1")
            log_file.close()
            with open("kde_setup_command.log", "a") as log_file:
                log_file.write(kde_setup_command + "run successfully")
                log_file.close()
    except os.error:
        print("Error setting up " + kde_setup_command)


# Setup VNStat
def vnstat_setup():
    interfaces = subprocess.run(["nmcli", "device", "status"], capture_output=True, text=True).stdout.splitlines()
    for interface in interfaces:
        # Open a file for logging
        log_file = open("output.log", "w")
        os.system("vnstat -u -i " + interface.split()[0]+" >> output.log 2>&1")
    os.system("systemctl enable vnstat >> output.log 2>&1")
    os.system("systemctl start vnstat >> output.log 2>&1")
    log_file.close()



# Ask User how they want to set up Fedora
def shitbox_setup():
    def download_ssh_key():
        dbx = dropbox.Dropbox(
            app_key='9qx5m6wmf51e811',
            app_secret='r4dcl1g70xg9a4i',
            oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
        )
        metadata, res = dbx.files_download(path='/ssh_keys.txt')
        with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'wb') as f:
            f.write(res.content)

    # Apply HAL9001 Public Key to authorized_keys
    def apply_ssh_key():
        # Create .ssh directory if it doesn't exist
        os.system("mkdir -p /home/{}/.ssh".format(user))
        os.system("mkdir -p /root/.ssh")
        # Create authorized_keys file if it doesn't exist
        os.system("touch /home/{}/.ssh/authorized_keys".format(user))
        os.system("touch /root/.ssh/authorized_keys")
        # Append HAL9001 Public Key to authorized_keys
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /home/{}/.ssh/authorized_keys".format(user, user))
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys".format(user))
        os.system("rm -rf /home/{}/Desktop/workspace/ssh_keys.txt".format(user))
        # Set permissions on authorized_keys
        os.system("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
        os.system("chmod 600 /root/.ssh/authorized_keys")

    # Set SSH to only allow key based authentication
    def set_ssh_config():
        os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
        os.system("systemctl restart sshd")

    def install_barrier():
        os.system("dnf -y install barrier")
        os.system("wget https://www.dropbox.com/s/s27nhs25i2r97pr/barrier.service?dl=1 -O barrier.service")
        os.system("cp barrier.service /etc/systemd/system/")
        os.system("chown root:root /etc/systemd/system/barrier.service")
        os.system("systemctl daemon-reload")
        os.system("systemctl enable barrier.service")
        os.system("systemctl start barrier.service")

    def download_files():
        # Download Konsave knsv file
        os.system(
            "wget  https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1" + " -O /home/{}/Desktop/workspace/{}.knsv".format(
                user, user))

    # Apply Konsave Theme
    def apply_theme():
        os.system("sudo -u {} konsave -w".format(user))
        os.system("sudo -u {} konsave -i /home/{}/Desktop/workspace/{}.knsv".format(user, user, user))
        os.system("sudo -u {} konsave -a /home/{}/Desktop/workspace/{}".format(user, user, user))
        
    # Run Shitbox Setup
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()
    install_barrier()
    download_files()
    apply_theme()


def fedorabox_setup():
    def download_ssh_key():
        dbx = dropbox.Dropbox(
            app_key='9qx5m6wmf51e811',
            app_secret='r4dcl1g70xg9a4i',
            oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
        )
        metadata, res = dbx.files_download(path='/ssh_keys.txt')
        with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'wb') as f:
            f.write(res.content)

    # Apply HAL9001 Public Key to authorized_keys
    def apply_ssh_key():
        # Create .ssh directory if it doesn't exist
        os.system("mkdir -p /home/{}/.ssh".format(user))
        os.system("mkdir -p /root/.ssh")
        # Create authorized_keys file if it doesn't exist
        os.system("touch /home/{}/.ssh/authorized_keys".format(user))
        os.system("touch /root/.ssh/authorized_keys")
        # Append HAL9001 Public Key to authorized_keys
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /home/{}/.ssh/authorized_keys".format(user, user))
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys".format(user))
        os.system("rm -rf /home/{}/Desktop/workspace/ssh_keys.txt".format(user))
        # Set permissions on authorized_keys
        os.system("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
        os.system("chmod 600 /root/.ssh/authorized_keys")

    # Set SSH to only allow key based authentication
    def set_ssh_config():
        os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
        os.system("systemctl restart sshd")

    def download_files():
        # Download Konsave knsv file
        os.system(
            "wget  https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1" + " -O /home/{}/Desktop/workspace/{}.knsv".format(
                user, user))

    # Apply Konsave Theme
    def apply_theme():
        os.system("sudo -u {} konsave -w".format(user))
        os.system("sudo -u {} konsave -i /home/{}/Desktop/workspace/{}.knsv".format(user, user, user))
        os.system("sudo -u {} konsave -a /home/{}/Desktop/workspace/{}".format(user, user, user))

    # Run Fedorabox Setup
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()
    download_files()
    apply_theme()


def hal9001_setup():
    # Create SSH Private/Public Key Pair
    def create_ssh_key():
        os.system("ssh-keygen -t rsa -b 4096 -C 'ramboy17@hotmail.com' -f /home/{}/.ssh/id_rsa -N ''".format(user))
        os.system("systemctl restart sshd")

    # Create ssh_keys.txt file from /root/.ssh/id_rsa.pub and /home/{}/.ssh/id_rsa.pub.format(user)
    def create_ssh_keys_txt():
        os.system("touch /home/{}/Dekstop/workspace/ssh_keys.txt".format(user))
        os.system("cat /root/.ssh/id_rsa.pub >> /home/{}/Dekstop/workspace/ssh_keys.txt".format(user))
        os.system("cat /home/{}/.ssh/id_rsa.pub >> /home/{}/Dekstop/workspace/ssh_keys.txt".format(user, user))
        os.system("chmod 600 /home/{}/Dekstop/workspace/ssh_keys.txt".format(user))

    # Upload ssh_keys.txt to Dropbox
    def upload_ssh_keys_txt():
        with open('/home/{}/Dekstop/workspace/ssh_keys.txt'.format(user), 'rb') as f:
            data = f.read()
        dbx = dropbox.Dropbox(
            app_key='9qx5m6wmf51e811',
            app_secret='r4dcl1g70xg9a4i',
            oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP')
        dbx.files_upload(data, '/ssh_keys.txt', mode=dropbox.files.WriteMode.overwrite)


    def download_files():
        # Download Konsave knsv file
        os.system(
            "wget  https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1" + " -O /home/{}/Desktop/workspace/{}.knsv".format(
                user, user))

    # Apply Konsave Theme
    def apply_theme():
        os.system("sudo -u {} konsave -w".format(user))
        os.system("sudo -u {} konsave -i /home/{}/Desktop/workspace/{}.knsv".format(user, user, user))
        os.system("sudo -u {} konsave -a /home/{}/Desktop/workspace/{}".format(user, user, user))


    # Run HAL9001 Setup
    create_ssh_key()
    create_ssh_keys_txt()
    upload_ssh_keys_txt()
    download_files()
    apply_theme()









def laptop_setup():
    def download_ssh_key():
        dbx = dropbox.Dropbox(
            app_key='9qx5m6wmf51e811',
            app_secret='r4dcl1g70xg9a4i',
            oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
        )
        metadata, res = dbx.files_download(path='/ssh_keys.txt')
        with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'wb') as f:
            f.write(res.content)

    # Apply HAL9001 Public Key to authorized_keys
    def apply_ssh_key():
        # Create .ssh directory if it doesn't exist
        os.system("mkdir -p /home/{}/.ssh".format(user))
        os.system("mkdir -p /root/.ssh")
        # Create authorized_keys file if it doesn't exist
        os.system("touch /home/{}/.ssh/authorized_keys".format(user))
        os.system("touch /root/.ssh/authorized_keys")
        # Append HAL9001 Public Key to authorized_keys
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /home/{}/.ssh/authorized_keys".format(user, user))
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys".format(user))
        os.system("rm -rf /home/{}/Desktop/workspace/ssh_keys.txt".format(user))
        # Set permissions on authorized_keys
        os.system("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
        os.system("chmod 600 /root/.ssh/authorized_keys")

    # Set SSH to only allow key based authentication
    def set_ssh_config():
        os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
        os.system("systemctl restart sshd")

    def download_files():
        # Download Konsave knsv file
        os.system(
            "wget  https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1" + " -O /home/{}/Desktop/workspace/{}.knsv".format(
                user, user))

    # Apply Konsave Theme
    def apply_theme():
        os.system("sudo -u {} konsave -w".format(user))
        os.system("sudo -u {} konsave -i /home/{}/Desktop/workspace/{}.knsv".format(user, user, user))
        os.system("sudo -u {} konsave -a /home/{}/Desktop/workspace/{}".format(user, user, user))


    # Run Laptop Setup
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()
    download_files()
    apply_theme()



def router_setup():
    def download_ssh_key():
        dbx = dropbox.Dropbox(
            app_key='9qx5m6wmf51e811',
            app_secret='r4dcl1g70xg9a4i',
            oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
        )
        metadata, res = dbx.files_download(path='/ssh_keys.txt')
        with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'wb') as f:
            f.write(res.content)

    # Apply HAL9001 Public Key to authorized_keys
    def apply_ssh_key():
        # Create .ssh directory if it doesn't exist
        os.system("mkdir -p /home/{}/.ssh".format(user))
        os.system("mkdir -p /root/.ssh")
        # Create authorized_keys file if it doesn't exist
        os.system("touch /home/{}/.ssh/authorized_keys".format(user))
        os.system("touch /root/.ssh/authorized_keys")
        # Append HAL9001 Public Key to authorized_keys
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /home/{}/.ssh/authorized_keys".format(user, user))
        os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys".format(user))
        os.system("rm -rf /home/{}/Desktop/workspace/ssh_keys.txt".format(user))
        # Set permissions on authorized_keys
        os.system("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
        os.system("chmod 600 /root/.ssh/authorized_keys")

    # Set SSH to only allow key based authentication
    def set_ssh_config():
        os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
        os.system("systemctl restart sshd")

    cdc_wdm_interfaces = []

    # Look for cdc-wdm* in nmcli device status
    def cdc_wdm():
        cellular_setup()
        interfaces = subprocess.run(["nmcli", "device", "status"], capture_output=True, text=True).stdout
        for line in interfaces.splitlines():
            if 'cdc-wdm' in line:
                cdc_wdm_interfaces.append(line.split()[0])
        if len(cdc_wdm_interfaces) > 0:
            print("Found the following cdc-wdm interfaces: {}".format(cdc_wdm_interfaces))
            cellular_setup()

    # Setup cellular interfaces
    def cellular_setup():
        external_zone_interfaces = []
        if len(cdc_wdm_interfaces) < 1:
            pass
        for i, interface in enumerate(cdc_wdm_interfaces):
            # Set cellular interface APN
            cellular_interface_apn = input('Enter the APN for interface {}: '.format(interface))
            # Set cellular interface username
            cellular_interface_username = input('Enter the username for interface {}: '.format(interface))
            if cellular_interface_username == '':
                # don't set username
                pass
            # Set cellular interface password
            cellular_interface_password = input('Enter the password for Interface {}: '.format(interface))
            if cellular_interface_password == '':
                # don't set password
                pass
            # Get Carrier Name
            carrier_name = input('Enter the carrier name for interface {}: '.format(interface))
            # append cdc_wdm_interface enumeral to Carrier Name (ex. 't-mobile1')
            carrier_name = carrier_name + str(i)
            # Create connection profile
            if cellular_interface_username == '' and cellular_interface_password == '':
                try:
                    os.system("nmcli connection add type gsm ifname {} con-name {} apn {} ".format(i, carrier_name,
                                                                                                   cellular_interface_apn))
                    os.system("nmcli connection modify {} autoconnect yes".format(carrier_name))
                    os.system("nmcli connection up {}".format(carrier_name))
                    # Check if connection is up
                    connection_status = os.popen("nmcli connection show {}".format(carrier_name)).read()
                    if 'connected' in connection_status:
                        # Append connection to configured_wwan_connections list
                        external_zone_interfaces.append(carrier_name)
                        cdc_wdm_interfaces.remove(i)
                    else:
                        print("Connection failed")

                except os.error:
                    print("Error creating connection attempting fcc_unlock()")
                    fcc_unlock()
                    cellular_setup()
            else:
                try:
                    os.system("nmcli connection add type gsm ifname {} con-name {} apn {} user {} password {}".format(i,
                                                                                                                      carrier_name,
                                                                                                                      cellular_interface_apn,
                                                                                                                      cellular_interface_username,
                                                                                                                      cellular_interface_password))
                    os.system("nmcli connection modify {} autoconnect yes".format(carrier_name))
                    os.system("nmcli connection up {}".format(carrier_name))
                    # Check if connection is up
                    connection_status = os.popen("nmcli connection show {}".format(carrier_name)).read()
                    if 'connected' in connection_status:
                        # Append connection to configured_wwan_connections list
                        external_zone_interfaces.append(carrier_name)
                        cdc_wdm_interfaces.remove(i)
                except os.error:
                    print("Error creating connection attempting fcc_unlock()")
                    fcc_unlock()

    # Watch journalctl for cdc-wdm interface and if journalctl shows 'Invalid transition for device' run fcc_unlock()
    def fcc_unlock():
        # Write last 100 lines of journalctl to journalctl.txt
        os.system("journalctl -n 100 > journalctl.txt")
        # Open journalctl.txt and read lines for 'NetworkManager[<number>]
        with open('journalctl.txt', 'r') as f:
            journalctl = f.read()
            if 'NetworkManager[' in journalctl:
                if 'modem-broadband[cdc-wdm{}]'.format(cdc_wdm_interfaces[0]) in journalctl:
                    if 'Invalid transition for device' in journalctl:
                        # Run fcc_unlock
                        os.system(
                            "qmicli -p -v -d /dev/cdc-wdm{} --device-open-mbim --dms-set-fcc-authentication".format(
                                cdc_wdm_interfaces[0]))
                        # Remove cdc_wdm_interfaces[0] from cdc_wdm_interfaces list
                        cdc_wdm_interfaces.remove(cdc_wdm_interfaces[0])
                        # Run cellular_setup()
                        cellular_setup()
                    else:
                        pass
                else:
                    pass
            else:
                pass
        # Remove journalctl.txt
        os.system("rm journalctl.txt")

    ethernet_interfaces = []

    # Get ethernet interfaces
    def get_ethernet_interfaces():
        interfaces = subprocess.run(['nmcli', '-t', '-f', 'DEVICE', 'device'], capture_output=True,
                                    text=True).stdout.strip().split('\n')
        for interface in interfaces:
            if interface != 'lo':
                ethernet_interfaces.append(interface)

    # Setup ethernet interfaces
    def ethernet_setup():
        import ipaddress
        external_zone_interfaces = []
        internal_ip_subnets = []
        interfaces_for_bridge = []
        if len(ethernet_interfaces) < 1:
            pass
        for i, interface in enumerate(ethernet_interfaces):
            ask_ethernet = input(
                'Would you like to configure interface {} as External, Internal, or Wifi AP Bridge? (E/I/W): '.format(
                    interface))
            if ask_ethernet == 'E' or ask_ethernet == 'e':
                try:
                    # Set ethernet interface ipv4.method auto and ipv6.method disabled
                    connection_name = input('Enter the connection name for interface {}: '.format(interface))
                    if connection_name == '':
                        connection_name = interface
                    elif connection_name.isalnum():
                        pass
                    elif len(connection_name) < 7 or len(connection_name) > 15:
                        print("Connection name must be between 7 and 15 characters")
                        ethernet_setup()
                    else:
                        print("Connection name must be alphanumeric")
                        ethernet_setup()
                    os.system(
                        "nmcli connection add type ethernet ifname {} con-name {} ipv4.method auto ipv6.method disabled".format(
                            interface, connection_name))
                    os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                    os.system("nmcli connection up {}".format(connection_name))
                    ethernet_interfaces.remove(interface)
                    external_zone_interfaces.append(connection_name)
                except os.error:
                    print("Error creating connection")
                    ethernet_setup()
            elif ask_ethernet == 'I' or ask_ethernet == 'i':
                # Ask User for IP Address and Netmask
                ip_address_netmask = input('Enter the IP Address for interface {}: '.format(interface))
                # Check if IP Address is valid using ipaddress module
                try:
                    ipaddress.ip_interface(ip_address_netmask)
                except ValueError:
                    print("Invalid IP Address")
                    ethernet_setup()
                # using nmcli set ethernet interface ipv4.method manual and ipv6.method disabled
                try:
                    # Set ethernet interface ipv4.method manual and ipv6.method disabled
                    connection_name = input('Enter the connection name for interface {}: '.format(interface))
                    if connection_name == '':
                        connection_name = interface
                    elif connection_name.isalnum():
                        pass
                    elif len(connection_name) < 7 or len(connection_name) > 15:
                        print("Connection name must be between 7 and 15 characters")
                        ethernet_setup()
                    else:
                        print("Connection name must be alphanumeric")
                        ethernet_setup()
                    os.system(
                        "nmcli connection add type ethernet ifname {} con-name {} ipv4.method manual ipv6.method disabled".format(
                            interface, connection_name))
                    os.system("nmcli connection modify {} ipv4.addresses {} ipv4.method manual".format(connection_name,
                                                                                                       ip_address_netmask))
                    os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                    os.system("nmcli connection up {}".format(connection_name))
                    ethernet_interfaces.remove(i)
                    external_zone_interfaces.append(connection_name)
                    internal_ip_subnets.append(ip_address_netmask)
                except os.error:
                    print("Error creating connection")
                    ethernet_setup()

            elif ask_ethernet == 'W' or ask_ethernet == 'w':
                try:
                    # Set ethernet interface ipv4.method manual and ipv6.method disabled
                    connection_name = input('Enter the connection name for interface {}: '.format(interface))
                    if connection_name == '':
                        connection_name = interface
                    elif connection_name.isalnum():
                        pass
                    elif len(connection_name) < 7 or len(connection_name) > 15:
                        print("Connection name must be between 7 and 15 characters")
                        ethernet_setup()
                    else:
                        print("Connection name must be alphanumeric")
                        ethernet_setup()
                    # append slave to connection name
                    connection_name = connection_name + ' slave'
                    os.system(
                        "nmcli connection add type ethernet ifname {} con-name {} ipv4.method manual ipv6.method disabled".format(
                            interface, connection_name))
                    os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                    os.system("nmcli connection up {}".format(connection_name))
                    ethernet_interfaces.remove(i)
                    interfaces_for_bridge.append(interface)
                except os.error:
                    print("Error creating connection")
                    ethernet_setup()

            else:
                print("Invalid Input")
                ethernet_setup()

    valid_banda_channels = ['32', '34', '36', '38', '40', '42', '44', '46', '48', '149', '151', '153', '155', '157',
                            '159',
                            '161', '165']
    valid_bandbg_channels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    wifi_interfaces = []

    # Get Wifi Interfaces
    def get_wifi_interfaces():
        interfaces = subprocess.run(['nmcli', 'device', 'status'], capture_output=True, text=True).stdout
        if "wifi" in interfaces:
            for line in interfaces.splitlines():
                if "wifi" in line:
                    wifi_interfaces.append(line.split()[0])
        else:
            print("No wifi interfaces found")
            return

    # Setup wifi interfaces
    def wifi_setup():
        import ipaddress
        import getpass
        interfaces_for_bridge = []
        internal_zone_interfaces = []
        internal_ip_subnets = []
        external_zone_interfaces = []
        if len(wifi_interfaces) < 1:
            pass
        for interface in wifi_interfaces:
            # Ask if user wants to configure wifi interface as Bridge AP, AP, or Client
            ask_wifi = input(
                'Would you like to configure interface {} as Bridge AP, AP, or Client? (B/A/C): '.format(interface))
            if ask_wifi == 'B' or ask_wifi == 'b':
                try:
                    # Set wifi interface ipv4.method manual and ipv6.method disabled
                    connection_name = input('Enter the connection name for interface {}: '.format(interface))
                    if connection_name == '':
                        connection_name = interface
                    elif connection_name.isalnum():
                        pass
                    elif len(connection_name) < 7 or len(connection_name) > 15:
                        print("Connection name must be between 7 and 15 characters")
                        wifi_setup()
                    else:
                        print("Connection name must be alphanumeric")
                        wifi_setup()
                    wifi_ssid = input('Enter the SSID for interface {}: '.format(interface))
                    if wifi_ssid == '':
                        wifi_ssid = interface
                    elif wifi_ssid.isalnum():
                        pass
                    elif len(wifi_ssid) < 7 or len(wifi_ssid) > 15:
                        print("SSID must be between 7 and 15 characters")
                        wifi_setup()
                    else:
                        print("SSID must be alphanumeric")
                        wifi_setup()
                    # wifi password must be between 8 and 63 characters and masked
                    wifi_password = getpass.getpass('Enter the password for interface {}: '.format(interface))
                    if len(wifi_password) < 8 or len(wifi_password) > 63:
                        print("Password must be between 8 and 63 characters")
                        wifi_setup()
                    elif wifi_password.isalnum():
                        pass
                    else:
                        print("Password must be alphanumeric")
                        wifi_setup()
                    # Ask user to select Wifi Band either a or bg
                    wifi_band = input('Enter the Wifi Band for interface {} (a or bg): '.format(interface))
                    if wifi_band == 'a':
                        wifi_band = 'a'
                    elif wifi_band == 'bg':
                        wifi_band = 'bg'
                    else:
                        print("Invalid Wifi Band")
                        wifi_setup()
                    # Ask user to select Wifi Channel
                    # If Wifi Band is a then channel must be in valid_banda_channels list
                    # If Wifi Band is bg then channel must be in valid_bandbg_channels list
                    wifi_channel = input('Enter the Wifi Channel for interface {}: '.format(interface))
                    if wifi_band == 'a':
                        if wifi_channel in valid_banda_channels:
                            valid_banda_channels.remove(wifi_channel)
                            pass
                        else:
                            print("Invalid Wifi Channel")
                            wifi_setup()
                    elif wifi_band == 'bg':
                        if wifi_channel in valid_bandbg_channels:
                            valid_bandbg_channels.remove(wifi_channel)
                            pass
                        else:
                            print("Invalid Wifi Channel")
                            wifi_setup()
                    else:
                        print("Invalid Wifi Band")
                        wifi_setup()
                    # append slave to connection name
                    connection_name = connection_name + ' slave'
                    os.system(
                        "nmcli connection add type wifi ifname {} con-name {} ssid {} wifi-sec.key-mgmt wpa-psk wifi-sec.psk {} 802-11-wireless.mode ap 802-11-wireless.band {} 802-11-wireless.channel {} ipv4.method shared ipv6.method disabled".format(
                            interface, connection_name, wifi_ssid, wifi_password, wifi_band, wifi_channel))
                    os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                    os.system("nmcli connection up {}".format(connection_name))
                    wifi_interfaces.remove(interface)
                    interfaces_for_bridge.append(interface)
                except os.error:
                    print("Error creating connection")
                    wifi_setup()
            elif ask_wifi == 'A' or ask_wifi == 'a':
                try:
                    # Set wifi interface ipv4.method manual and ipv6.method disabled
                    connection_name = input('Enter the connection name for interface {}: '.format(interface))
                    if connection_name == '':
                        connection_name = interface
                    elif connection_name.isalnum():
                        pass
                    elif len(connection_name) < 7 or len(connection_name) > 15:
                        print("Connection name must be between 7 and 15 characters")
                        wifi_setup()
                    else:
                        print("Connection name must be alphanumeric")
                        wifi_setup()
                    wifi_ssid = input('Enter the SSID for interface {}: '.format(interface))
                    if wifi_ssid == '':
                        wifi_ssid = interface
                    elif wifi_ssid.isalnum():
                        pass
                    elif len(wifi_ssid) < 7 or len(wifi_ssid) > 15:
                        print("SSID must be between 7 and 15 characters")
                        wifi_setup()
                    else:
                        print("SSID must be alphanumeric")
                        wifi_setup()
                    # wifi password must be between 8 and 63 characters and masked
                    wifi_password = getpass.getpass('Enter the password for interface {}: '.format(interface))
                    if len(wifi_password) < 8 or len(wifi_password) > 63:
                        print("Password must be between 8 and 63 characters")
                        wifi_setup()
                    elif wifi_password.isalnum():
                        pass
                    else:
                        print("Password must be alphanumeric")
                        wifi_setup()
                    # Ask user to select Wifi Band either a or bg
                    wifi_band = input('Enter the Wifi Band for interface {} (a or bg): '.format(interface))
                    if wifi_band == 'a':
                        wifi_band = 'a'
                    elif wifi_band == 'bg':
                        wifi_band = 'bg'
                    else:
                        print("Invalid Wifi Band")
                        wifi_setup()
                    # Ask user to select Wifi Channel
                    # If Wifi Band is a then channel must be in valid_banda_channels list
                    # If Wifi Band is bg then channel must be in valid_bandbg_channels list
                    wifi_channel = input('Enter the Wifi Channel for interface {}: '.format(interface))
                    if wifi_band == 'a':
                        if wifi_channel in valid_banda_channels:
                            valid_banda_channels.remove(wifi_channel)
                            pass
                        else:
                            print("Invalid Wifi Channel")
                            wifi_setup()
                    elif wifi_band == 'bg':
                        if wifi_channel in valid_bandbg_channels:
                            valid_bandbg_channels.remove(wifi_channel)
                            pass
                        else:
                            print("Invalid Wifi Channel")
                            wifi_setup()
                    else:
                        print("Invalid Wifi Band")
                        wifi_setup()
                    wifi_ip_and_mask = input('Enter the IP address and mask for interface {}: '.format(interface))
                    if wifi_ip_and_mask == '':
                        wifi_ip_and_mask = '192.168.255.1/24'
                        # validate with ipaddress module
                        try:
                            ipaddress.ip_network(wifi_ip_and_mask, strict=False)
                        except ValueError:
                            print("Invalid IP address and mask")
                            wifi_setup()
                    else:
                        # validate with ipaddress module
                        try:
                            ipaddress.ip_network(wifi_ip_and_mask, strict=False)
                        except ValueError:
                            print("Invalid IP address and mask")
                            wifi_setup()
                    # use nmcli to create wifi connection
                    os.system(
                        "nmcli connection add type wifi ifname {} con-name {} ssid {} wifi-sec.key-mgmt wpa-psk wifi-sec.psk {} 802-11-wireless.mode ap 802-11-wireless.band {} 802-11-wireless.channel {} ipv4.method manual ipv4.addresses {} ipv6.method disabled".format(
                            interface, connection_name, wifi_ssid, wifi_password, wifi_band, wifi_channel,
                            wifi_ip_and_mask))
                    os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                    os.system("nmcli connection up {}".format(connection_name))
                    wifi_interfaces.remove(interface)
                    internal_zone_interfaces.append(interface)
                    internal_ip_subnets.append(wifi_ip_and_mask)
                except os.error:
                    print("Error creating connection")
                    wifi_setup()
            elif ask_wifi == 'C' or ask_wifi == 'c':
                try:
                    # Use nmcli to list wifi access points and show them to the user in a numbered list
                    # User selects the access point they want to connect to
                    # User enters the password for the access point
                    # Use nmcli to create wifi connection
                    wifi_ap_list = os.popen("nmcli device wifi list").read()
                    for i, line in enumerate(wifi_ap_list.splitlines()):
                        print(i, line)
                    wifi_ap = input('Enter the number of the access point you want to connect to: ')
                    wifi_ap = int(wifi_ap)
                    if wifi_ap in range(0, len(wifi_ap_list)):
                        pass
                    else:
                        print("Invalid access point")
                        wifi_setup()
                    wifi_password = getpass.getpass('Enter the password for interface {}: '.format(interface))
                    if len(wifi_password) < 8 or len(wifi_password) > 63:
                        print("Password must be between 8 and 63 characters")
                        wifi_setup()
                    elif wifi_password.isalnum():
                        pass
                    else:
                        print("Password must be alphanumeric")
                        wifi_setup()
                    os.system("nmcli device wifi connect {} password {}".format(wifi_ap_list[wifi_ap], wifi_password))
                    wifi_interfaces.remove(interface)
                    external_zone_interfaces.append(interface)
                    # Get the IP address and mask for the interface append to internal_ip_subnets list
                    ip_subnet = os.popen("ip addr show {}".format(interface)).read()
                    ip_subnet = ip_subnet.splitlines()[2].split()[1]
                    internal_ip_subnets.append(ip_subnet)
                except os.error:
                    print("Error connecting to access point")
                    wifi_setup()
            else:
                print("Invalid selection")
                wifi_setup()
        else:
            pass


    # Run Router Setup
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()
    cdc_wdm()
    cellular_setup()
    fcc_unlock()
    get_ethernet_interfaces()
    ethernet_setup()
    get_wifi_interfaces()
    wifi_setup()


def bridge_setup():
    import ipaddress
    interfaces_for_bridge = []
    internal_ip_subnets = []
    internal_zone_interfaces = []
    # Ask the user if they want to create a bridge
    bridge_question = input('Do you want to create a bridge? (Y/N): ')
    if bridge_question == 'Y' or bridge_question == 'y':
        print(interfaces_for_bridge)
        # Ask the user to select the interfaces they want to add to the bridge from the interfaces_for_bridge list
        bridge_slave1 = input('Enter the first interface you want to add to the bridge: ')
        if bridge_slave1 in interfaces_for_bridge:
            pass
        else:
            print("Invalid interface")
            bridge_setup()
        bridge_slave2 = input('Enter the second interface you want to add to the bridge: ')
        if bridge_slave2 in interfaces_for_bridge:
            pass
        else:
            print("Invalid interface")
            bridge_setup()
        # Ask the user to enter the name of the bridge
        bridge_connection_name = input('Enter the name of the bridge: ')
        if bridge_connection_name == '':
            print("Invalid bridge name")
            bridge_setup()
        elif bridge_connection_name.isalnum():
            pass
        elif bridge_connection_name == 'lo':
            print("Invalid bridge name")
            bridge_setup()
        elif len(bridge_connection_name) < 1 or len(bridge_connection_name) > 15:
            print("Invalid bridge name")
            bridge_setup()
        else:
            print("Invalid bridge name")
            bridge_setup()
        # Ask the user for bridge interface name
        bridge_interface_name = input('Enter the name of the bridge interface, must be something like "br0": ')
        # bridge_interface_name must start with br and end with a number ex. br0
        if bridge_interface_name == '':
            bridge_interface_name = 'br0'
        elif bridge_interface_name.startswith('br') and bridge_interface_name[2:].isdigit():
            pass
        else:
            print("Invalid bridge interface name")
            bridge_setup()
        # Ask the user for bridge IP address and mask
        bridge_ip_and_mask = input(
            'Enter the IP address and mask for the bridge interface {}: '.format(bridge_interface_name))
        # Validate bridge_ip_and_mask with ipaddress module
        try:
            ipaddress.ip_network(bridge_ip_and_mask, strict=False)
        except ValueError:
            print("Invalid IP address and mask")
            bridge_setup()
        # Use nmcli to create bridge connection
        os.system(
            "nmcli connection add type bridge ifname {} con-name {} ipv4.method manual ipv4.addresses {} ipv6.method disabled".format(
                bridge_interface_name, bridge_connection_name, bridge_ip_and_mask))
        os.system("nmcli connection modify {} autoconnect yes".format(bridge_connection_name))
        os.system("nmcli connection up {}".format(bridge_connection_name))
        # Use nmcli to add bridge slaves
        os.system(
            "nmcli connection add type bridge-slave ifname {} master {}".format(bridge_slave1, bridge_connection_name))
        os.system(
            "nmcli connection add type bridge-slave ifname {} master {}".format(bridge_slave2, bridge_connection_name))
        # Remove the bridge slaves from the interfaces_for_bridge list
        interfaces_for_bridge.remove(bridge_slave1)
        interfaces_for_bridge.remove(bridge_slave2)
        # Add the bridge interface to the internal_ip_subnets list
        internal_ip_subnets.append(bridge_ip_and_mask)
        internal_zone_interfaces.append(bridge_interface_name)
        # Ask the user if they want to create another bridge
        bridge_question = input('Do you want to create another bridge? (Y/N): ')
        if bridge_question == 'Y' or bridge_question == 'y':
            bridge_setup()
        else:
            pass
    else:
        pass

    # variables
    internal_zone_interfaces = []
    internal_ip_subnets = []
    external_zone_interfaces = []

    # Get Hostname
    def get_hostname():
        hostname = input("Enter the hostname: ")
        return hostname

    # If hostname contains router run router_setup() else run firewall_setup()
    def router_or_firewall():
        hostname = get_hostname()
        if "router" in hostname:
            router_setup()
        else:
            host_setup()

    def router_setup():
        enable_ip_forwarding()
        setup_masquerade()
        setup_named_conf()
        setup_dhcp_server()
        setup_firewall()

    def host_setup():
        import netifaces
        # set all interfaces as external
        for interface in netifaces.interfaces():
            external_zone_interfaces.append(interface)
        setup_firewall()

    # Enable IP Forwarding
    def enable_ip_forwarding():
        os.system("echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf")
        os.system("sysctl -p")
        os.system("sysctl -w net.ipv4.ip_forward=1")
        setup_masquerade()

    # Setup MASQUERADE and Filter Forwarding
    def setup_masquerade():
        for e in external_zone_interfaces:
            for i in internal_zone_interfaces:
                os.system(
                    "firewall-cmd --permanent --direct --add-rule ipv4 nat POSTROUTING 0 -o {} -j MASQUERADE".format(e))
                os.system(
                    "firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i {} -o {} -j ACCEPT".format(i,
                                                                                                                      e))
                os.system(
                    "firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i {} -o {} -m state --state RELATED,ESTABLISHED -j ACCEPT".format(
                        e, i))
                os.system("firewall-cmd --reload")
        setup_named_conf()

    # Setup named.conf
    def setup_named_conf():
        os.system("systemctl stop named")
        os.system("rm /etc/named.conf")
        os.system("touch /etc/named.conf")
        os.system("echo 'options {' >> /etc/named.conf")
        # For every subnet in internal_subnets, add a listen-on
        # Using the ipaddress module to get the first ip address in the subnet
        for i in internal_ip_subnets:
            ip = ipaddress.ip_network(i)
            ip = ip[1]
            os.system("echo 'listen-on port 53 {{ {} }};' >> /etc/named.conf".format(ip))
        # For every subnet in internal_subnets, add a allow-query
        for i in internal_ip_subnets:
            os.system("echo 'allow-query {{ {} }};' >> /etc/named.conf".format(i))
        # add an allow-recursion
        for i in internal_ip_subnets:
            os.system("echo 'allow-recursion {{ {} }};' >> /etc/named.conf".format(i))
        # append localhost to allow query line
        os.system("echo 'allow-query {{ localhost; }};' >> /etc/named.conf")
        # append localhost to allow recursion line
        os.system("echo 'allow-recursion {{ localhost; }};' >> /etc/named.conf")
        # append 127.0.0.1 to listen on line
        os.system("echo 'listen-on port 53 {{ 127.0.0.1; }};' >> /etc/named.conf")
        # append forwarders
        forwarders = "8.8.8.8", "8.8.4.4"
        for i in forwarders:
            os.system("echo 'forwarders {{ {} }};' >> /etc/named.conf".format(i))
        # append recursion yes
        os.system("echo 'recursion yes;' >> /etc/named.conf")
        # append forward only
        os.system("echo 'forward only;' >> /etc/named.conf")
        # close options
        os.system("echo '};' >> /etc/named.conf")
        # Restart named
        os.system("systemctl start named")
        os.system("systemctl enable named")
        setup_dhcp_server()

    # Setup DHCP Server
    def setup_dhcp_server():
        os.system("systemctl stop dhcpd")
        os.system("rm /etc/dhcp/dhcpd.conf")
        os.system("touch /etc/dhcp/dhcpd.conf")
        # Using the ipaddress module to get the first ip and last ip in the subnet
        for i in internal_ip_subnets:
            ip = ipaddress.ip_network(i)
            ip_first = ip[1]
            ip_last = ip[-1]
            os.system("echo 'subnet {} netmask {} {{' >> /etc/dhcp/dhcpd.conf".format(ip_first, ip.netmask))
            os.system("echo 'range {} {};' >> /etc/dhcp/dhcpd.conf".format(ip_first, ip_last))
            os.system("echo 'option routers {};' >> /etc/dhcp/dhcpd.conf".format(ip_first))
            os.system("echo 'option domain-name-servers {};' >> /etc/dhcp/dhcpd.conf".format(ip_first))
            os.system("echo '}}' >> /etc/dhcp/dhcpd.conf")
        # Restart dhcpd
        os.system("systemctl start dhcpd")
        os.system("systemctl enable dhcpd")

    # Setup Firewall
    def setup_firewall():
        # Add zones
        os.system("firewall-cmd --permanent --new-zone=internal")
        os.system("firewall-cmd --permanent --new-zone=external")
        # Add interfaces to zones
        for i in internal_zone_interfaces:
            os.system("firewall-cmd --permanent --zone=internal --add-interface={}".format(i))
        for e in external_zone_interfaces:
            os.system("firewall-cmd --permanent --zone=external --add-interface={}".format(e))

    def run_airsonic_installer():
        # Run Airsonic Installer
        os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/airsonic_installer.py".format(user))

    # Run Jellyfin Installer
    def run_jellyfin_installer():
        # Run Jellyfin Installer
        os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/jellyfin_installer.py".format(user))

    # Run Nextcloud Installer
    def run_nextcloud_installer():
        # Run Nextcloud Installer
        os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/nextcloud_installer.py".format(user))

    # variables
    failover_priority = []

    # Using the external_zone_interfaces list, ask user to select each interface in order of failover priority, append to failover_priority list
    def set_failover_priority():
        if len(external_zone_interfaces) < 1:
            pass
        else:
            print(external_zone_interfaces)
            failover = input(
                'Enter the interface {} in order of failover priority: (First entry will have highest priority, Last entry will have lowest. ')
            if failover in external_zone_interfaces:
                failover_priority.append(failover)
                external_zone_interfaces.remove(failover)
                if len(external_zone_interfaces) > 0:
                    set_failover_priority()
                else:
                    print("Failover priority set")
            else:
                print("Invalid interface")
                set_failover_priority()
            print(failover_priority)
        ask_confirm_priority = input('Are you satisfied with the failover priority? (Y/N): If not we will start over. ')
        if ask_confirm_priority == 'Y' or ask_confirm_priority == 'y':
            set_wan_failover_service()
        else:
            failover_priority.clear()
            set_failover_priority()

    # Set the wan failover.py script as a service that runs on boot
    def set_wan_failover_service():
        os.system("cp /home/{}/wan_failover.py /etc/wan_failover.py".format(user))
        os.system("chmod +x /etc/wan_failover.py")
        os.system("chown root:root /etc/wan_failover.py")
        os.system("chmod 755 /etc/wan_failover.py")
        create_wan_failover_service()

    # Create a service file for the wan failover.py script
    def create_wan_failover_service():
        os.system("touch /etc/systemd/system/wan_failover.service")
        os.system("echo '[Unit]' >> /etc/systemd/system/wan_failover.service")
        os.system("echo 'Description=wan_failover' >> /etc/systemd/system/wan_failover.service")
        os.system("echo 'After=network.target' >> /etc/systemd/system/wan_failover.service")
        os.system("echo '' >> /etc/systemd/system/wan_failover.service")
        os.system("echo '[Service]' >> /etc/systemd/system/wan_failover.service")
        os.system("echo 'Type=simple' >> /etc/systemd/system/wan_failover.service")
        os.system("echo 'ExecStart=/usr/bin/python3 /etc/wan_failover.py' >> /etc/systemd/system/wan_failover.service")
        os.system("echo '' >> /etc/systemd/system/wan_failover.service")
        os.system("echo '[Install]' >> /etc/systemd/system/wan_failover.service")
        os.system("echo 'WantedBy=multi-user.target' >> /etc/systemd/system/wan_failover.service")
        os.system("systemctl daemon-reload")
        os.system("systemctl enable wan_failover.service")
        os.system("systemctl start wan_failover.service")

    # Run the functions
    router_or_firewall()
    setup_firewall()
    set_failover_priority()
    run_airsonic_installer()
    run_jellyfin_installer()
    run_nextcloud_installer()



def fed_type():
    # Get hostname from hostnamectl
    hostname = os.popen("hostnamectl | grep hostname | awk '{print $3}'").read()
    # Open a file for logging
    log_file = open("output.log", "w")
    if "fedorabox" in hostname:
        os.system("wget -O fedboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedboxmotd.txt >> output.log 2>&1")
        os.system("echo fedboxmotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
        fedorabox_setup()
    elif "hal9001" in hostname:
        os.system("wget -O hal9001motd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedhal9k1motd.txt >> output.log 2>&1")
        os.system("echo hal9001motd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
        hal9001_setup()
    elif "laptop" in hostname:
        os.system("wget -O laptopmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedlaptopmotd.txt >> output.log 2>&1")
        os.system("echo laptopmotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
        laptop_setup()
    elif "router" in hostname:
        os.system("wget -O routermotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedroutermotd.txt >> output.log 2>&1")
        os.system("echo routermotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
        router_setup()
    elif "shitbox" in hostname:
        os.system("wget -O shitboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/shitboxmotd.txt >> output.log 2>&1")
        os.system("echo shitboxmotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
        shitbox_setup()
    else:
        print("Invalid Input")
        log_file.close()


# Main Function
def main():
    run_function("add_repos")
    run_function("install_groups")
    run_function("install_packages")
    run_function("install_network_packages")
    run_function("install_pip_packages")
    run_function("configure_applications")
    run_function("install_chrome")
    run_function("install_vscode")
    run_function("new_user")
    run_function("setup_workspace")
    run_function("install_pycharm")
    run_function("download_files")
    run_function("download_nomachine")
    run_function("install_zsh")
    run_function("start_sddm")
    run_function("create_usbethernet_connection")
    run_function("avahi_setup")
    run_function("vnstat_setup")
    run_function("kde_setup")
    run_function("fed_type")


if __name__ == '__main__':
    main()
