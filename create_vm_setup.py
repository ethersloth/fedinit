#!/bin/python3

# Import modules
import os
import requests
from bs4 import BeautifulSoup
from external_drive import disk_name
import subprocess
user = ''

# Pull user variable from user.txt
def get_user():
    global user
    hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout
    with open("/home/{}/Desktop/workspace/{}config/user.txt".format(user, hostname)) as f:
        user = f.read()
        print("User: {}".format(user))


# Create ISO folder in mount point
def create_iso_folder():
    os.system("mkdir /home/{}/Desktop/workspace/{}/ISOs".format(user, disk_name))


# Create VM folder in mount point
def create_vm_folder():
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs".format(user, disk_name))


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
    os.system("mv " + iso_link + " /home/{}/Desktop/workspace/{}/ISOs/fedora.iso".format(user, disk_name))
    # Create Fedora VM Folder in VMs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs/fedora".format(user, disk_name))
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
    os.system("mv *.iso" + "/home/{}/Desktop/workspace/{}/ISOs/centos.iso".format(user, disk_name))
    # Create CentOS VM Folder in VMs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs/centos".format(user, disk_name))
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
    os.system("mv *.iso" + "/home/{}/Desktop/workspace/{}/ISOs/ubuntu.iso".format(user, disk_name))
    # Create Ubuntu VM Folder in VMs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs/ubuntu".format(user, disk_name))
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
    os.system("mv *.iso" + "/home/{}/Desktop/workspace/{}/ISOs/debian.iso".format(user, disk_name))
    # Create Debian VM Folder in VMs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs/debian".format(user, disk_name))
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
    os.system("mv *.iso" + "/home/{}/Desktop/workspace/{}/ISOs/rocky.iso".format(user, disk_name))
    # Create Rocky VM Folder in VMs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs/rocky".format(user, disk_name))
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
    os.system("mv *.iso" + "/home/{}/Desktop/workspace/{}/ISOs/rhel.iso".format(user, disk_name))
    # Create RHEL VM Folder in VMs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}/VMs/rhel".format(user, disk_name))


# Create VMs
def create_vms():
    # Create Fedora VM, 4 CPU, 4GB RAM, 100GB HDD in VMs folder. Make sure VM is reachable via SSH, VNCSERVER is running, and the VM is running.
    os.system("virt-install --name fedora --ram 4096 --vcpus 4 --disk path=/home/{}/Desktop/workspace/{}/VMs/fedora/fedora.qcow2,size=100 --cdrom /home/{}/Desktop/workspace/{}/ISOs/fedora.iso --network bridge=br0 --graphics vnc,listen=5900 --os-type linux --os-variant fedora33 --noautoconsole --vnc --vncport 5900 --vncpassword fedora".format(user, disk_name, user, disk_name))
    # Create CentOS VM, 4 CPU, 4GB RAM, 100GB HDD in VMs folder. Make sure VM is reachable via SSH, VNCSERVER is running, and the VM is running.
    os.system("virt-install --name centos --ram 4096 --vcpus 4 --disk path=/home/{}/Desktop/workspace/{}/VMs/centos/centos.qcow2,size=100 --cdrom /home/{}/Desktop/workspace/{}/ISOs/centos.iso --network bridge=br0 --graphics vnc,listen=5901 --os-type linux --os-variant centos9 --noautoconsole --vnc --vncport 5901 --vncpassword centos".format(user, disk_name, user, disk_name))
    # Create Ubuntu VM, 4 CPU, 4GB RAM, 100GB HDD in VMs folder. Make sure VM is reachable via SSH, VNCSERVER is running, and the VM is running.
    os.system("virt-install --name ubuntu --ram 4096 --vcpus 4 --disk path=/home/{}/Desktop/workspace/{}/VMs/ubuntu/ubuntu.qcow2,size=100 --cdrom /home/{}/Desktop/workspace/{}/ISOs/ubuntu.iso --network bridge=br0 --graphics vnc,listen=5902 --os-type linux --os-variant ubuntu22.10 --noautoconsole --vnc --vncport 5902 --vncpassword ubuntu".format(user, disk_name, user, disk_name))
    # Create Debian VM, 4 CPU, 4GB RAM, 100GB HDD in VMs folder. Make sure VM is reachable via SSH, VNCSERVER is running, and the VM is running.
    os.system("virt-install --name debian --ram 4096 --vcpus 4 --disk path=/home/{}/Desktop/workspace/{}/VMs/debian/debian.qcow2,size=100 --cdrom /home/{}/Desktop/workspace/{}/ISOs/debian.iso --network bridge=br0 --graphics vnc,listen=5903 --os-type linux --os-variant debian11 --noautoconsole --vnc --vncport 5903 --vncpassword debian".format(user, disk_name, user, disk_name))
    # Create Rocky VM, 4 CPU, 4GB RAM, 100GB HDD in VMs folder. Make sure VM is reachable via SSH, VNCSERVER is running, and the VM is running.
    os.system("virt-install --name rocky --ram 4096 --vcpus 4 --disk path=/home/{}/Desktop/workspace/{}/VMs/rocky/rocky.qcow2,size=100 --cdrom /home/{}/Desktop/workspace/{}/ISOs/rocky.iso --network bridge=br0 --graphics vnc,listen=5904 --os-type linux --os-variant rocky9 --noautoconsole --vnc --vncport 5904 --vncpassword rocky".format(user, disk_name, user, disk_name))
    # Create RHEL VM, 4 CPU, 4GB RAM, 100GB HDD in VMs folder. Make sure VM is reachable via SSH, VNCSERVER is running, and the VM is running.
    os.system("virt-install --name rhel --ram 4096 --vcpus 4 --disk path=/home/{}/Desktop/workspace/{}/VMs/rhel/rhel.qcow2,size=100 --cdrom /home/{}/Desktop/workspace/{}/ISOs/rhel.iso --network bridge=br0 --graphics vnc,listen=5905 --os-type linux --os-variant rhel9 --noautoconsole --vnc --vncport 5905 --vncpassword rhel".format(user, disk_name, user, disk_name))


# Main Function
def main():
    # Get user
    get_user()
    # Create VMs Folder
    create_vms()
    # Download Fedora ISO
    download_fed_iso()
    # Download CentOS ISO
    download_centos_iso()
    # Download Ubuntu ISO
    download_ubuntu_iso()
    # Download Debian ISO
    download_debian_iso()
    # Download Rocky ISO
    download_rocky_iso()
    # Download RHEL ISO
    download_rhel_iso()
    # Create VMs
    create_vms()


if __name__ == "__main__":
    main()

