#!/bin/python3
import os

from fedinitinstall import user


# Run konsave.py
def apply_theme():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/konsave.py".format(user))


# Install Barrier
def install_barrier():
    os.system("dnf -y install barrier")


# appy_hal9k1_ssh_key.py
def get_ssh_key():
    os.system("/bin/python3 /home/{}/Dekstop/workspace/Scripts/appy_hal9k1_ssh_key.py".format(user))


# External Drive
def mount_external_drive():
    os.system("/bin/python3 /home/{}/Dekstop/workspace/Scripts/external_drive.py".format(user))


# Setup Firewall
def setup_firewall():
    os.system("/bin/python3 /home/{}/Dekstop/workspace/Scripts/firewall_setup.py".format(user))


def setup_vpn():
    input("Would you like to setup a VPN? (Y/N)")
    if input == 'Y':
        # Ask user if they want to setup an IPSec VPN or OpenVPN
        input("Would you like to setup an IPSec VPN or OpenVPN? (I/O)")
        if input == 'I':
            os.system("python3 /home/{}/Dekstop/workspace/Scripts/ipsec_vpn.py".format(user))
        elif input == 'O':
            os.system("python3 /home/{}/Dekstop/workspace/Scripts/openvpnclient.py".format(user))
        else:
            print("Invalid input. Not setting up VPN.")
            setup_vpn()
    elif input == 'N':
        print("Not setting up VPN.")
    else:
        print("Invalid input. Not setting up VPN.")
        setup_vpn()


# Wan Failover
def setup_wan_failover():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/wan_failover.py".format(user))


# Main Function
def main():
    apply_theme()
    install_barrier()
    get_ssh_key()
    mount_external_drive()
    setup_firewall()
    setup_vpn()
    setup_wan_failover()


if __name__ == '__main__':
    main()
