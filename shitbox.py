#!/bin/python3

import os

from fedinitinstall import user

disk_name = ''


# Run apply_hal9k1_ssh_key.py
def apply_hal9k1_ssh_key():
    os.system("python3 /home/{}/Desktop/workspace/Scripts/apply_hal9k1_ssh_key.py".format(user))


# Run External Drive.py
def external_drive():
    os.system("python3 /home/{}/Desktop/workspace/Scripts/external_drive.py".format(user))


# Run Firewall.py
def firewall():
    os.system("python3 /home/{}/Desktop/workspace/Scripts/firewall_setup.py".format(user))


# Install Barrier, pull down barrier service, enable and start service
def install_barrier():
    os.system("dnf -y install barrier")
    os.system("wget https://www.dropbox.com/s/s27nhs25i2r97pr/barrier.service?dl=1 -O barrier.service")
    os.system("cp barrier.service /etc/systemd/system/")
    os.system("chown root:root /etc/systemd/system/barrier.service")
    os.system("systemctl daemon-reload")
    os.system("systemctl enable barrier.service")
    os.system("systemctl start barrier.service")


# Create VM Setup
def create_vm_setup():
    os.system("python3 /home/{}/Desktop/workspace/Scripts/create_vm_setup.py".format(user))


# Ask user if they want to setup WAN Failover
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


# Main function
def main():
    # Run apply_hal9k1_ssh_key.py
    apply_hal9k1_ssh_key()

    # Run External Drive.py
    external_drive()

    # Run Firewall.py
    firewall()

    # Install Barrier, pull down barrier service, enable and start service
    install_barrier()

    # Create VM Setup
    create_vm_setup()

    # Ask user if they want to setup WAN Failover
    setup_wan_failover()

    # Ask user if they want to setup a VPN (IPSec or OpenVPN)
    setup_vpn()

    # Run Config Parser
    run_config_parser()


if __name__ == "__main__":
    main()
