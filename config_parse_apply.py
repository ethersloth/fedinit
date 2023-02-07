#!/bin/python3

# This script is for parsing the system_config zip file and applying any changes to the system

import os
import zipfile
import shutil


# View the contents of the zip file
def view_zip_contents():
    with zipfile.ZipFile("system_config.zip", 'r') as zip_ref:
        zip_ref.printdir()

        # If fstab.txt exists, compare the contents of the file to the current fstab file
        # If the contents are different, overwrite the current fstab file with the contents of the zip file
        # If the contents are the same, do nothing
        if os.path.exists("system_config/fstab/fstab.txt"):
            with open("system_config/fstab/fstab.txt", "r") as zip_fstab:
                with open("/etc/fstab", "r") as current_fstab:
                    if zip_fstab.read() != current_fstab.read():
                        shutil.copyfile("system_config/fstab/fstab.txt", "/etc/fstab")
                        print("fstab.txt has been updated")
                    else:
                        print("fstab.txt is up to date")
        else:
            print("fstab.txt does not exist")

        # If there are any file in the system_config/network_interfaces directory, compare the contents of the files to the current network interfaces files
        # If the contents are different, overwrite the current network interfaces files with the contents of the zip files
        # If the contents are the same, do nothing
        if os.path.exists("system_config/network_interfaces"):
            for file in os.listdir("system_config/network_interfaces"):
                with open("system_config/network_interfaces/" + file, "r") as zip_network_interfaces:
                    with open("/etc/network/interfaces.d/" + file, "r") as current_network_interfaces:
                        if zip_network_interfaces.read() != current_network_interfaces.read():
                            shutil.copyfile("system_config/network_interfaces/" + file,
                                            "/etc/network/interfaces.d/" + file)
                            print(file + " has been updated")
                        else:
                            print(file + " is up to date")

        # If there are any file in the system_config/openvpn directory, compare the contents of the files to the current openvpn files
        # If the contents are different, overwrite the current openvpn files with the contents of the zip files
        # If the contents are the same, do nothing
        if os.path.exists("system_config/openvpn"):
            for file in os.listdir("system_config/openvpn"):
                with open("system_config/openvpn/" + file, "r") as zip_openvpn:
                    with open("/etc/openvpn/" + file, "r") as current_openvpn:
                        if zip_openvpn.read() != current_openvpn.read():
                            shutil.copyfile("system_config/openvpn/" + file, "/etc/openvpn/" + file)
                            print(file + " has been updated")
                        else:
                            print(file + " is up to date")

        # If there are any files in the system_config/ipsec directory, compare the contents of the files to the current ipsec files
        # If the contents are different, overwrite the current ipsec files with the contents of the zip files
        # If the contents are the same, do nothing
        if os.path.exists("system_config/ipsec"):
            for file in os.listdir("system_config/ipsec"):
                with open("system_config/ipsec/" + file, "r") as zip_ipsec:
                    with open("/etc/ipsec.d/" + file, "r") as current_ipsec:
                        if zip_ipsec.read() != current_ipsec.read():
                            shutil.copyfile("system_config/ipsec/" + file, "/etc/ipsec.d/" + file)
                            print(file + " has been updated")
                        else:
                            print(file + " is up to date")

        # If there are any files in the system_config/wireguard directory, compare the contents of the files to the current wireguard files
        # If the contents are different, overwrite the current wireguard files with the contents of the zip files
        # If the contents are the same, do nothing
        if os.path.exists("system_config/wireguard"):
            for file in os.listdir("system_config/wireguard"):
                with open("system_config/wireguard/" + file, "r") as zip_wireguard:
                    with open("/etc/wireguard/" + file, "r") as current_wireguard:
                        if zip_wireguard.read() != current_wireguard.read():
                            shutil.copyfile("system_config/wireguard/" + file, "/etc/wireguard/" + file)
                            print(file + " has been updated")
                        else:
                            print(file + " is up to date")

        # If there are any files in the system_config/dhcpd directory, compare the contents of the files to the current dhcpd files
        # If the contents are different, overwrite the current dhcpd files with the contents of the zip files
        # If the contents are the same, do nothing
        if os.path.exists("system_config/dhcpd"):
            for file in os.listdir("system_config/dhcpd"):
                with open("system_config/dhcpd/" + file, "r") as zip_dhcpd:
                    with open("/etc/dhcpd/" + file, "r") as current_dhcpd:
                        if zip_dhcpd.read() != current_dhcpd.read():
                            shutil.copyfile("system_config/dhcpd/" + file, "/etc/dhcpd/" + file)
                            print(file + " has been updated")
                        else:
                            print(file + " is up to date")

        # If there are any files in the system_config/firewalld directory, compare the contents of the files to the current firewalld files
        # If the contents are different, overwrite the current firewalld files with the contents of the zip files
        # If the contents are the same, do nothing
        if os.path.exists("system_config/firewalld"):
            for file in os.listdir("system_config/firewalld"):
                with open("system_config/firewalld/" + file, "r") as zip_firewalld:
                    with open("/etc/firewalld/" + file, "r") as current_firewalld:
                        if zip_firewalld.read() != current_firewalld.read():
                            shutil.copyfile("system_config/firewalld/" + file, "/etc/firewalld/" + file)
                            print(file + " has been updated")
                        else:
                            print(file + " is up to date")

        # If the system_config directory does not exist, create it
        else:
            os.mkdir("system_config")
            print("system_config directory created")

    # If the system_config/dhcpd directory does not exist, create it
    if not os.path.exists("system_config/dhcpd"):
        os.mkdir("system_config/dhcpd")
        print("system_config/dhcpd directory created")

    # If the system_config/firewalld directory does not exist, create it
    if not os.path.exists("system_config/firewalld"):
        os.mkdir("system_config/firewalld")
        print("system_config/firewalld directory created")

    # If the system_config/ipsec directory does not exist, create it
    if not os.path.exists("system_config/ipsec"):
        os.mkdir("system_config/ipsec")
        print("system_config/ipsec directory created")

    # If the system_config/network_interfaces directory does not exist, create it
    if not os.path.exists("system_config/network_interfaces"):
        os.mkdir("system_config/network_interfaces")
        print("system_config/network_interfaces directory created")

    # If the system_config/openvpn directory does not exist, create it
    if not os.path.exists("system_config/openvpn"):
        os.mkdir("system_config/openvpn")
        print("system_config/openvpn directory created")

    # If the system_config/wireguard directory does not exist, create it
    if not os.path.exists("system_config/wireguard"):
        os.mkdir("system_config/wireguard")
        print("system_config/wireguard directory created")

    # If the system_config/wireguard directory does not exist, create it
    if not os.path.exists("system_config/wireguard"):
        os.mkdir("system_config/wireguard")
        print("system_config/wireguard directory created")
