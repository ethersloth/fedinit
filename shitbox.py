#!/bin/python3

import os
import psutil
import requests
from bs4 import BeautifulSoup
import dropbox


# Download SSH Public Key From Dropbox
def download_ssh_key():
    dbx = dropbox.Dropbox('sl.BX3VVSTTHKAg2tQvY5LLIEbgtwW29pRUaQl6KbgklwKQI98ZWt2UPXXFLhstXSPYDZJQcB0L9jHlS-FwAZk7ybl0JPeUT1w8zcKqzZAwBcf0TRtPBZcARLaVzRtwJ4HJNiMeb9g')
    metadata, res = dbx.files_download(path='/ssh_keys.txt')
    with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'wb') as f:
        f.write(res.content)


# Apply HAL9001 Public Key to authorized_keys
def apply_ssh_key():
    os.system("cat /home/gwhitlock/Desktop/workspace/ssh_keys.txt >> /home/gwhitlock/.ssh/authorized_keys")
    os.system("cat /home/gwhitlock/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys")
    os.system("rm -rf /home/gwhitlock/Desktop/workspace/ssh_keys.txt")


# Set SSH to only allow key based authentication
def set_ssh_config():
    os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    os.system("systemctl restart sshd")


# Install Barrier, pull down barrier service, enable and start service
def install_barrier():
    os.system("dnf -y install barrier")
    os.system("wget -N https://www.dropbox.com/s/s27nhs25i2r97pr/barrier.service?dl=1 -O barrier.service")
    os.system("cp barrier.service /etc/systemd/system/")
    os.system("systemctl daemon-reload")
    os.system("systemctl enable barrier.service")
    os.system("systemctl start barrier.service")
    install_kvm()


# Make sure KVM is installed
def install_kvm():
    os.system("dnf -y install qemu-kvm libvirt virt-install bridge-utils virt-manager")
    os.system("systemctl enable libvirtd")
    os.system("systemctl start libvirtd")
    download_files()


def download_files():
    os.system("wget -N https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1 -O gwhitlock.knsv")
    apply_theme()


# Apply Konsave Theme
def apply_theme():
    os.system("konsave -i gwhitlock.knsv")
    mount_drive()


# List Unmounted Drives, select drive to mount, mount drive
def get_unmounted_drives():
    drives = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'cdrom' in partition.opts or partition.fstype == '':
            # skip cd-rom drives with no disk in it; they may raise an exception
            continue
        try:
            if os.path.ismount(partition.mountpoint):
                continue
            else:
                drives.append(partition.device)
        except PermissionError:
            pass
    mount_drive()
    return drives


# From get_unmounted_drives() return a list of unmounted drives, ask the user if they want to mount a drive, if yes, ask user to select a drive to mount
def mount_drive():
    drives = get_unmounted_drives()
    if len(drives) == 0:
        print("No unmounted drives found")
        exit(1)
    else:
        print("The following drives are unmounted:")
        for i in range(len(drives)):
            print(str(i) + ": " + drives[i])
        choice = input("Would you like to mount a drive? (y/n): ")
        if choice == "y":
            drive = input("Enter the number of the drive you would like to mount: ")
            while not drive.isdigit() or int(drive) < 0 or int(drive) > len(drives):
                drive = input("Invalid drive number. Enter a valid drive number: ")
                # Ask User for the mount point
            mount_point = input("Enter the mount point: ")
            if not os.path.exists(mount_point):
                os.system("mkdir " + mount_point)
                # format the drive with ext4
                os.system("parted " + drives[int(drive)] + " mklabel msdos")
                os.system("parted " + drives[int(drive)] + " mkpart primary ext4 0% 100%")
                os.system("mkfs.ext4 " + drives[int(drive)] + "1")
                # mount the drive
                os.system("mount " + drives[int(drive)] + "1 " + mount_point)
                # add the drive to /etc/fstab
                os.system("echo " + drives[int(drive)] + "1 " + mount_point + " ext4 defaults 0 0 >> /etc/fstab")
                print("Drive mounted successfully")
                create_iso_folder()
                return mount_point

        else:
            print("Mounting drive failed")


# Create ISO folder in mount point
def create_iso_folder():
    mount_point = mount_drive()
    os.system("mkdir " + mount_point + "/ISOs")
    print("ISO folder created successfully")
    download_fed_iso()


# Download ISOs
def download_fed_iso():
    mount_point = mount_drive()
    url = "https://download.fedoraproject.org/pub/fedora/linux/releases"
    response = requests.get(url)

    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the link to the latest ISO
    iso_link = None
    for link in soup.find_all('a'):
        if link.get('href').endswith('.iso') and 'x86_64' in link.get('href') and 'Everything' in link.get('href'):
            iso_link = link.get('href')
            break

    # Download the ISO
    if iso_link:
        iso_url = f'{url}/{iso_link}'
        response = requests.get(iso_url, stream=True)
        with open(iso_link, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f'Successfully downloaded {iso_link}')
    else:
        print('Could not find the link to the latest ISO')
    # Move ISO to ISO folder
    os.system("mv " + iso_link + " " + mount_point + "/ISOs/fedora.iso")
    download_centos_iso()


# Download CentOS ISO
def download_centos_iso():
    mount_point = mount_drive()
    url = "https://mirrors.centos.org/mirrorlist?path=/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-dvd1.iso&redirect=1&protocol=https"
    response = requests.get(url, stream=True)

    with open("CentOS-Stream-9-latest-x86_64-dvd1.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv CentOS-Stream-9-latest-x86_64-dvd1.iso " + mount_point + "/ISOs/centos.iso")
    download_ubuntu_iso()


# Download Ubuntu ISO
def download_ubuntu_iso():
    mount_point = mount_drive()
    url = "https://releases.ubuntu.com/22.10/ubuntu-22.10-desktop-amd64.iso"
    response = requests.get(url, stream=True)

    with open("ubuntu-22.10-desktop-amd64.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv ubuntu-*-desktop-amd64.iso " + mount_point + "/ISOs/ubuntu.iso")
    download_debian_iso()


# Download Debian ISO
def download_debian_iso():
    mount_point = mount_drive()

    url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-11.6.0-amd64-netinst.iso"
    response = requests.get(url, stream=True)

    with open("debian-11.6.0-amd64-netinst.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv debian-*-amd64-netinst.iso " + mount_point + "/ISOs/debian.iso")
    download_rocky_iso()


# Download Rocky ISO
def download_rocky_iso():
    mount_point = mount_drive()

    url = "https://download.rockylinux.org/pub/rocky/9/isos/x86_64/Rocky-9.1-x86_64-minimal.iso"
    response = requests.get(url, stream=True)

    with open("Rocky-9.1-x86_64-minimal.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv Rocky-*-x86_64-minimal.iso " + mount_point + "/ISOs/rocky.iso")
    download_rhel_iso()


# Download RHEL ISO
def download_rhel_iso():
    mount_point = mount_drive()

    url = "https://developers.redhat.com/content-gateway/file/rhel/9.1/rhel-baseos-9.1-x86_64-dvd.iso"
    response = requests.get(url, stream=True)

    with open("rhel-baseos-9.1-x86_64-dvd.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv rhel-*.iso " + mount_point + "/ISOs/rhel.iso")


# Run other python scripts
def run_scripts():
    os.system("/bin/python3 kvm_vm_create.py")
    os.system("/bin/python3 openvpnser.py")
    os.system("/bin/python3 config_grabber.py")


# Main function
def main():
    mount_drive()
    create_iso_folder()
    download_fed_iso()
    download_centos_iso()
    download_ubuntu_iso()
    download_debian_iso()
    download_rocky_iso()
    download_rhel_iso()
    run_scripts()