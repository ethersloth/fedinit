#!/bin/python3

import os
from shitbox import mount_drive


def create_vm():
    name = input("Enter the name of the VM: ")
    if os.path.isfile(mount_drive() + name + ".qcow2"):
        print("VM already exists.")
        name = input("Enter the name of the VM: ")
    ram = input("Enter the amount of RAM (in MB): ")
    if ram.isdigit():
        print("Invalid RAM amount.")
        ram = input("Enter the amount of RAM (in MB): ")
    elif ram < "1024":
        print("RAM amount is too low.")
        ram = input("Enter the amount of RAM (in MB): ")
    elif ram > "4096":
        print("RAM amount is too high.")
        ram = input("Enter the amount of RAM (in MB): ")
    cpu = input("Enter the number of CPUs: ")
    if cpu.isdigit():
        print("Invalid CPU amount.")
        cpu = input("Enter the number of CPUs: ")
    elif cpu < "1":
        print("CPU amount is too low.")
        cpu = input("Enter the number of CPUs: ")
    elif cpu > "4":
        print("CPU amount is too high.")
        cpu = input("Enter the number of CPUs: ")
    os_type = input("Enter the OS type: ")
    os_variant = input("Enter the OS variant: ")
    location = mount_drive() + name + ".iso"
    vm_image_location = mount_drive() + name + ".qcow2"

    os.system(
        "virt-install --name={} --ram={} --vcpus={} --disk path={},size=100 --os-type={} --os-variant={} --network bridge=br0 --graphics vnc,listen=5900 --console pty,target_type=serial --location '{}' --extra-args 'console=ttyS0,115200n8 serial' --noreboot".format(
            name, ram, cpu, vm_image_location, os_type, os_variant, location))

    print("VM created successfully.")


# Main
def main():
    create_vm()


if __name__ == "__main__":
    main()
