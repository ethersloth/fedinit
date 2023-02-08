#!/bin/python3
import os
from fedinitinstall import user

# variables
disk_name = ''


# Apply HAL9001 Public Key to authorized_keys
def apply_ssh_key():
    os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/apply_hal9k1_ssh_key.py".format(user))


# Setup External Disk
def setup_external_disk():
    # Run External Disk Setup
    os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/external_disk.py".format(user))


# Setup Firewall
def setup_firewall():
    # Run Firewall Setup
    os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/firewall.py".format(user))


def setup_wan_failover():
    from fedinitinstall import user
    input("Would you like to setup WAN Failover? (Y/N)")
    if input == 'Y' or input == 'y':
        os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/wan_failover_setup.py".format(user))
    elif input == 'N' or input == 'n':
        print("Not setting up WAN Failover.")
        exit(1)
    else:
        print("Invalid input. Not setting up WAN Failover.")
        setup_wan_failover()


# Ask user if they want to setup a VPN (IPSec or OpenVPN)
def setup_vpn():
    from fedinitinstall import user
    input("Would you like to setup a VPN? (Y/N)")
    if input == 'Y' or input == 'y':
        # Ask user if they want to setup an IPSec VPN or OpenVPN
        input("Would you like to setup an IPSec VPN or OpenVPN? (I/O)")
        if input == 'I' or input == 'i':
            os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/ipsec_vpn.py".format(user))
        elif input == 'O' or input == 'o':
            os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/openvpnclient.py".format(user))
        else:
            print("Invalid input. Not setting up VPN.")
            setup_vpn()
    elif input == 'N' or input == 'n':
        print("Not setting up VPN.")
        exit(1)
    else:
        print("Invalid input. Not setting up VPN.")
        setup_vpn()


# Run Config Parser
def run_config_parser():
    # Run Config Parser
    os.system("/bin/python3 /home/gwhitlock/Desktop/workspace/Scripts/config_parser.py")


# Run Airsonic Installer
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


# Main function
def main():
    apply_ssh_key()
    setup_external_disk()
    setup_firewall()
    setup_wan_failover()
    setup_vpn()
    run_config_parser()
    run_airsonic_installer()
    run_jellyfin_installer()
    run_nextcloud_installer()