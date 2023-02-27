#!/bin/python3
import os
import re
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
    for group in groups:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("dnf groupinstall -y '{}' >> output.log 2>&1".format(group + '\n'))
            # Write group to group install log file
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
                "python3-pip"
    ]
    for package in packages:
        try:
            # Open a file for logging
            log_file = open("output.log", "w")
            os.system("dnf install -y {} >> output.log 2>&1".format(package + '\n'))
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
            os.system("dnf install -y {} >> output.log 2>&1".format(package + '\n'))
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
    import requests
    global user
    current_version = "1.27.2.13801"
    download_url = "https://download.jetbrains.com/toolbox/jetbrains-toolbox-latest.tar.gz"
    version_pattern = r"toolbox-(\d+\.\d+\.\d+\.\d+)\.tar\.gz"
    response = requests.get(download_url)

    # Extract the URL of the latest version of the tar file from the response
    url = response.url

    # Extract the version number from the URL using the provided pattern
    version = re.search(version_pattern, url).group(1)

    # Check if the version number matches the current version
    if version == current_version:
        print("The file is already up to date.")
        return

    # Download the file
    with open(f"jetbrains-toolbox-{version}.tar.gz", "wb") as f:
        f.write(response.content)
        f.close()
    print(f"File {version} downloaded successfully.")
    # Remove the version number from the file name
    # Open a file for logging
    log_file = open("output.log", "w")
    os.rename(f"jetbrains-toolbox-{version}.tar.gz", "jetbrains-toolbox.tar.gz >> output.log 2>&1")
    # Extract the tar file
    os.system("tar -xzf jetbrains-toolbox.tar.gz -C /opt >> output.log 2>&1")
    os.system("rm jetbrains-toolbox.tar.gz >> output.log 2>&1")
    os.system("mv /opt/jetbrains-toolbox-* /opt/jetbrains-toolbox >> output.log 2>&1")
    # make jetbrains-toolbox executable
    os.system("chmod +x /opt/jetbrains-toolbox/jetbrains-toolbox >> output.log 2>&1")
    # let the user run jetbrains-toolbox without sudo
    os.system(f"echo '{user} ALL=(ALL) NOPASSWD: /opt/jetbrains-toolbox/jetbrains-toolbox' >> /etc/sudoers >> output.log 2>&1")
    # add jetbrains-toolbox to path
    os.system("ln -s /opt/jetbrains-toolbox/jetbrains-toolbox /usr/bin/jetbrains-toolbox >> output.log 2>&1")
    log_file.close()


# Download files
def download_files():
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("wget -O .zshrc https://www.dropbox.com/s/y6zleax42iow846/.zshrc?dl=1 >> output.log 2>&1")
    os.system("wget -O .zshrc-root https://www.dropbox.com/s/afc0vm9dpde519c/.zshrc-root?dl=1 >> output.log 2>&1")
    log_file.close()


# Download and Install NoMachine
def download_nomachine():
    import requests
    global user
    current_version = "6.12.2_1"
    download_url = "https://download.nomachine.com/download/6.12/Linux/nomachine_6.12.2_1_x86_64.rpm"
    version_pattern = r"nomachine_(\d+\.\d+\.\d+_\d+)_x86_64\.rpm"
    response = requests.get(download_url)

    # Extract the URL of the latest version of the tar file from the response
    url = response.url

    # Extract the version number from the URL using the provided pattern
    version = re.search(version_pattern, url).group(1)

    # Check if the version number matches the current version
    if version == current_version:
        print("The file is already up to date.")
        return

    # Download the file
    with open(f"nomachine_{version}_x86_64.rpm", "wb") as f:
        f.write(response.content)
        f.close()
    print(f"File {version} downloaded successfully.")
    # Remove the version number from the file name
    # Open a file for logging
    log_file = open("output.log", "w")
    os.rename(f"nomachine_{version}_x86_64.rpm", "nomachine.rpm >> output.log 2>&1")
    # local install nomachine
    os.system("dnf -y localinstall nomachine.rpm >> output.log 2>&1")
    log_file.close()


# Install ZSH Config
def install_zsh():
    global user
    # Open a file for logging
    log_file = open("output.log", "w")
    os.system("cp .zshrc /home/" + user + "/.zshrc >> output.log 2>&1")
    os.system("cp .zshrc-root /root/.zshrc >> output.log 2>&1")
    os.system("chsh -s /bin/zsh " + user + " >> output.log 2>&1")
    os.system("chsh -s /bin/zsh root >> output.log 2>&1")
    log_file.close()


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
    elif "hal9001" in hostname:
        os.system("wget -O hal9001motd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedhal9k1motd.txt >> output.log 2>&1")
        os.system("echo hal9001motd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
    elif "laptop" in hostname:
        os.system("wget -O laptopmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedlaptopmotd.txt >> output.log 2>&1")
        os.system("echo laptopmotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
    elif "router" in hostname:
        os.system("wget -O routermotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/fedroutermotd.txt >> output.log 2>&1")
        os.system("echo routermotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
    elif "shitbox" in hostname:
        os.system("wget -O shitboxmotd.txt "
                  "https://raw.githubusercontent.com/gregredliontest/fedinstallscripts/main/shitboxmotd.txt >> output.log 2>&1")
        os.system("echo shitboxmotd.txt >> /etc/motd >> output.log 2>&1")
        log_file.close()
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
    run_function("start_sddm")
    run_function("install_nomachine")
    run_function("create_usbethernet_connection")
    run_function("avahi_setup")
    run_function("vnstat_setup")
    run_function("kde_setup")
    run_function("fed_type")


if __name__ == '__main__':
    main()
