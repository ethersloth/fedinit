#!/bin/python3

# import modules
import os
import subprocess

# variables
disk_name = ""


# List Unmounted Drives, select drive to mount, mount drive
def list_drives():
    result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'], capture_output=True, text=True)
    if result.returncode != 0:
        print('Error listing drives')
        return
    # Parse the output of lsblk
    output = result.stdout.strip().split('\n')
    # Extract the headers
    headers = output[0].split()
    # Extract the data
    data = [row.split() for row in output[1:]]
    # Create a list of dictionaries
    drives = []
    for row in data:
        drives.append(dict(zip(headers, row)))
    # Return the list of drives
    return drives


# Show Unmounted Drives
def show_drives():
    # List the disks (i.e sdb not sdb1)
    disks = list_drives()
    # Print the disks
    for i, disk in enumerate(disks):
        print(f'{i}. {disk["device"]}')
        # Make sure disk does not have a mountpoint of /boot, /home or / (root)
        if disk["mountpoint"] == "/boot" or disk["mountpoint"] == "/home" or disk["mountpoint"] == "/":
            print("This disk is already mounted")
            return
    # Ask the user to select a disk
    disk = disks[int(input('Select a disk: '))]
    # delete all partitions on disk
    os.system(f"parted -s {disk['device']} mklabel msdos")
    # create 1 partition on disk
    os.system(f"parted -s {disk['device']} mkpart primary ext4 0% 100%")
    # format partition
    os.system(f"mkfs.ext4 {disk['device']}1")
    # Ask User for the External Disk name, make sure it is alphanumeric
    global disk_name
    disk_name = input("Enter the name of the external disk: ")
    while not disk_name.isalnum():
        disk_name = input("Enter the name of the external disk: ")
    # Create mount point in /home/{username}/Desktop/workspace/{disk_name}
    os.system(f"mkdir /home/gwhitlock/Desktop/workspace/{disk_name}")
    # Mount the disk
    os.system(f"mount {disk['device']}1 /home/gwhitlock/Desktop/workspace/{disk_name}")
    # Add the disk to /etc/fstab
    os.system(f"echo '{disk['device']}1 /home/gwhitlock/Desktop/workspace/{disk_name} ext4 defaults 0 0' >> /etc/fstab")


# Main Function
def main():
    show_drives()
    print(f"Disk {disk_name} has been mounted")


# Run the main function
if __name__ == '__main__':
    main()