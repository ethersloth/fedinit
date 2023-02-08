#!/bin/python3

import os

from fedinitinstall import user

disk_name = ''


# Run Apply_hal9k1_ssh_key.py
def apply_ssh_key():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/apply_hal9k1_ssh_key.py".format(user))


# Run Konsave.py
def konsave():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/konsave.py".format(user))


# Run External_Drive.py
def external_drive():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/external_drive.py".format(user))


# Run Firewall.py
def firewall():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/firewall_setup.py".format(user))


# Ask user if they want to setup VPN (IPSec or OpenVPN)
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


# Ask user if they want to setup WAN Failover
def setup_wan_failover():
    from fedinitinstall import user
    input("Would you like to setup WAN Failover? (Y/N)")
    if input == 'Y':
        os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/wan_failover.py".format(user))
    elif input == 'N':
        print("Not setting up WAN Failover.")
    else:
        print("Invalid input. Not setting up WAN Failover.")
        setup_wan_failover()


# Run Config Parser
def run_config_parser():
    # Run Config Parser
    os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/config_parser.py".format(user))


# Create the main function
def main():
    # Run the functions
    apply_ssh_key()
    konsave()
    external_drive()
    firewall()
    setup_vpn()
    setup_wan_failover()
    run_config_parser()
