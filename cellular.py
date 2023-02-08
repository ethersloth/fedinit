#!/bin/python3
import os
import subprocess

from firewall_setup import external_zone_interfaces

cdc_wdm_interfaces = []


# Look for cdc-wdm* in nmcli device status
def cdc_wdm():
    cellular_setup()
    interfaces = subprocess.run(["nmcli", "device", "status"], capture_output=True, text=True).stdout
    for line in interfaces.splitlines():
        if 'cdc-wdm' in line:
            cdc_wdm_interfaces.append(line.split()[0])
    if len(cdc_wdm_interfaces) > 0:
        print("Found the following cdc-wdm interfaces: {}".format(cdc_wdm_interfaces))
        cellular_setup()


# Setup cellular interfaces
def cellular_setup():
    if len(cdc_wdm_interfaces) < 1:
        pass
    for i, interface in enumerate(cdc_wdm_interfaces):
        # Set cellular interface APN
        cellular_interface_apn = input('Enter the APN for interface {}: '.format(interface))
        # Set cellular interface username
        cellular_interface_username = input('Enter the username for interface {}: '.format(interface))
        if cellular_interface_username == '':
            # don't set username
            pass
        # Set cellular interface password
        cellular_interface_password = input('Enter the password for Interface {}: '.format(interface))
        if cellular_interface_password == '':
            # don't set password
            pass
        # Get Carrier Name
        carrier_name = input('Enter the carrier name for interface {}: '.format(interface))
        # append cdc_wdm_interface enumeral to Carrier Name (ex. 't-mobile1')
        carrier_name = carrier_name + str(i)
        # Create connection profile
        if cellular_interface_username == '' and cellular_interface_password == '':
            try:
                os.system("nmcli connection add type gsm ifname {} con-name {} apn {} ".format(i, carrier_name,
                                                                                               cellular_interface_apn))
                os.system("nmcli connection modify {} autoconnect yes".format(carrier_name))
                os.system("nmcli connection up {}".format(carrier_name))
                # Check if connection is up
                connection_status = os.popen("nmcli connection show {}".format(carrier_name)).read()
                if 'connected' in connection_status:
                    # Append connection to configured_wwan_connections list
                    external_zone_interfaces.append(carrier_name)
                    cdc_wdm_interfaces.remove(i)
                else:
                    print("Connection failed")

            except os.error:
                print("Error creating connection attempting fcc_unlock()")
                fcc_unlock()
                cellular_setup()
        else:
            try:
                os.system("nmcli connection add type gsm ifname {} con-name {} apn {} user {} password {}".format(i,
                                                                                                                  carrier_name,
                                                                                                                  cellular_interface_apn,
                                                                                                                  cellular_interface_username,
                                                                                                                  cellular_interface_password))
                os.system("nmcli connection modify {} autoconnect yes".format(carrier_name))
                os.system("nmcli connection up {}".format(carrier_name))
                # Check if connection is up
                connection_status = os.popen("nmcli connection show {}".format(carrier_name)).read()
                if 'connected' in connection_status:
                    # Append connection to configured_wwan_connections list
                    external_zone_interfaces.append(carrier_name)
                    cdc_wdm_interfaces.remove(i)
            except os.error:
                print("Error creating connection attempting fcc_unlock()")
                fcc_unlock()


# Watch journalctl for cdc-wdm interface and if journalctl shows 'Invalid transition for device' run fcc_unlock()
def fcc_unlock():
    # Write last 100 lines of journalctl to journalctl.txt
    os.system("journalctl -n 100 > journalctl.txt")
    # Open journalctl.txt and read lines for 'NetworkManager[<number>]
    with open('journalctl.txt', 'r') as f:
        journalctl = f.read()
        if 'NetworkManager[' in journalctl:
            if 'modem-broadband[cdc-wdm{}]'.format(cdc_wdm_interfaces[0]) in journalctl:
                if 'Invalid transition for device' in journalctl:
                    # Run fcc_unlock
                    os.system("qmicli -p -v -d /dev/cdc-wdm{} --device-open-mbim --dms-set-fcc-authentication".format(
                        cdc_wdm_interfaces[0]))
                    # Remove cdc_wdm_interfaces[0] from cdc_wdm_interfaces list
                    cdc_wdm_interfaces.remove(cdc_wdm_interfaces[0])
                    # Run cellular_setup()
                    cellular_setup()
                else:
                    pass
            else:
                pass
        else:
            pass
    # Remove journalctl.txt
    os.system("rm journalctl.txt")


# Main Function
def main():
    cdc_wdm()


# run main
if __name__ == '__main__':
    main()
