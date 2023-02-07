#!/bin/python3

import os

import dropbox
import requests
from bs4 import BeautifulSoup

drives = []


# Download SSH Public Key From Dropbox
def download_ssh_key():
    dbx = dropbox.Dropbox(
        'sl.BX3VVSTTHKAg2tQvY5LLIEbgtwW29pRUaQl6KbgklwKQI98ZWt2UPXXFLhstXSPYDZJQcB0L9jHlS-FwAZk7ybl0JPeUT1w8zcKqzZAwBcf0TRtPBZcARLaVzRtwJ4HJNiMeb9g')
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
def list_unmounted_drives():
    with open("/proc/mounts", "r") as mounts_file:
        mounted_drives = [line.split()[0] for line in mounts_file]

    unmounted_drives = []
    for device in os.listdir("/dev"):
        if device.startswith("sd") and "/dev/{device}" not in mounted_drives:
            unmounted_drives.append(f"/dev/{device}")

    return unmounted_drives


def get_unmounted_drives():
    unmounted_drives = list_unmounted_drives()
    if unmounted_drives:
        print("Unmounted drives:")
        for drive in unmounted_drives:
            print(drive)
    else:
        print("No unmounted drives found.")


# From get_unmounted_drives() return a list of unmounted drives, ask the user if they want to mount a drive, if yes, ask user to select a drive to mount
def mount_drive():
    get_unmounted_drives()
    unmounted_drives = list_unmounted_drives()
    if unmounted_drives:
        print("Do you want to mount a drive? (y/n)")
        answer = input()
        if answer == "y":
            print("Select a drive to mount:")
            for drive in unmounted_drives:
                print(drive)
            drive = input()
            if drive in unmounted_drives:
                os.system("mkdir /media/" + drive)
                os.system("mount " + drive + " /media/" + drive)
                print("Drive mounted successfully")
                create_iso_folder()
            else:
                print("Invalid drive")
                mount_drive()
        else:
            print("Drive not mounted")
            create_iso_folder()
    else:
        print("No unmounted drives found")
        create_iso_folder()


# Create ISO folder in mount point
def create_iso_folder():
    os.system("mkdir /media/sdb1/ISOs")
    download_fed_iso()


# Download ISOs
def download_fed_iso():
    # Get the HTML of the page
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
    os.system("mv " + iso_link + " /media/sdb1/ISOs/fedora.iso")
    download_centos_iso()


# Download CentOS ISO
def download_centos_iso():
    # Get the HTML of the page
    url = "https://mirrors.centos.org/mirrorlist?path=/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-dvd1.iso&redirect=1&protocol=https"
    response = requests.get(url, stream=True)

    with open("CentOS-Stream-9-latest-x86_64-dvd1.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv CentOS-*-latest-x86_64-dvd1.iso /media/sdb1/ISOs/centos.iso")
    download_ubuntu_iso()


# Download Ubuntu ISO
def download_ubuntu_iso():
    # Get the HTML of the page
    url = "https://releases.ubuntu.com/22.10/ubuntu-22.10-desktop-amd64.iso"
    response = requests.get(url, stream=True)

    with open("ubuntu-22.10-desktop-amd64.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv ubuntu-*-desktop-amd64.iso /media/sdb1/ISOs/ubuntu.iso")
    download_debian_iso()


# Download Debian ISO
def download_debian_iso():
    # Get the HTML of the page
    url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-11.6.0-amd64-netinst.iso"
    response = requests.get(url, stream=True)

    with open("debian-11.6.0-amd64-netinst.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv debian-*-amd64-netinst.iso /media/sdb1/ISOs/debian.iso")
    download_rocky_iso()


# Download Rocky ISO
def download_rocky_iso():
    # Get the HTML of the page
    url = "https://download.rockylinux.org/pub/rocky/9/isos/x86_64/Rocky-9.1-x86_64-minimal.iso"
    response = requests.get(url, stream=True)

    with open("Rocky-9.1-x86_64-minimal.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv Rocky-*-x86_64-minimal.iso /media/sdb1/ISOs/rocky.iso")
    download_rhel_iso()


# Download RHEL ISO
def download_rhel_iso():
    # Get the HTML of the page
    url = "https://developers.redhat.com/content-gateway/file/rhel/9.1/rhel-baseos-9.1-x86_64-dvd.iso"
    response = requests.get(url, stream=True)

    with open("rhel-baseos-9.1-x86_64-dvd.iso", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    print("Successfully downloaded the ISO.")
    # Move ISO to ISO folder
    os.system("mv rhel-*-x86_64-dvd.iso /media/sdb1/ISOs/rhel.iso")


# Run other python scripts
def run_scripts():
    os.system("/bin/python3 kvm_vm_create.py")
    os.system("/bin/python3 openvpnser.py")
    os.system("/bin/python3 config_grabber.py")


# Main function
def main():
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()
    install_kvm()
    mount_drive()
    run_scripts()


if __name__ == "__main__":
    main()
