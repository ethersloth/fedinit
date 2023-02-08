#!/bin/python3

# Import modules
import os
import ipaddress
import subprocess

from firewall_setup import internal_ip_subnets, interfaces_for_bridge, external_zone_interfaces

ethernet_interfaces = []


# Get ethernet interfaces
def get_ethernet_interfaces():
    interfaces = subprocess.run(['nmcli', '-t', '-f', 'DEVICE', 'device'], capture_output=True, text=True).stdout.strip().split('\n')
    for interface in interfaces:
        if interface != 'lo':
            ethernet_interfaces.append(interface)


# Setup ethernet interfaces
def ethernet_setup():
    if len(ethernet_interfaces) < 1:
        pass
    for i, interface in enumerate(ethernet_interfaces):
        ask_ethernet = input(
            'Would you like to configure interface {} as External, Internal, or Wifi AP Bridge? (E/I/W): '.format(
                interface))
        if ask_ethernet == 'E' or ask_ethernet == 'e':
            try:
                # Set ethernet interface ipv4.method auto and ipv6.method disabled
                connection_name = input('Enter the connection name for interface {}: '.format(interface))
                if connection_name == '':
                    connection_name = interface
                elif connection_name.isalnum():
                    pass
                elif len(connection_name) < 7 or len(connection_name) > 15:
                    print("Connection name must be between 7 and 15 characters")
                    ethernet_setup()
                else:
                    print("Connection name must be alphanumeric")
                    ethernet_setup()
                os.system(
                    "nmcli connection add type ethernet ifname {} con-name {} ipv4.method auto ipv6.method disabled".format(
                        interface, connection_name))
                os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                os.system("nmcli connection up {}".format(connection_name))
                ethernet_interfaces.remove(interface)
                external_zone_interfaces.append(connection_name)
            except os.error:
                print("Error creating connection")
                ethernet_setup()
        elif ask_ethernet == 'I' or ask_ethernet == 'i':
            # Ask User for IP Address and Netmask
            ip_address_netmask = input('Enter the IP Address for interface {}: '.format(interface))
            # Check if IP Address is valid using ipaddress module
            try:
                ipaddress.ip_interface(ip_address_netmask)
            except ValueError:
                print("Invalid IP Address")
                ethernet_setup()
            # using nmcli set ethernet interface ipv4.method manual and ipv6.method disabled
            try:
                # Set ethernet interface ipv4.method manual and ipv6.method disabled
                connection_name = input('Enter the connection name for interface {}: '.format(interface))
                if connection_name == '':
                    connection_name = interface
                elif connection_name.isalnum():
                    pass
                elif len(connection_name) < 7 or len(connection_name) > 15:
                    print("Connection name must be between 7 and 15 characters")
                    ethernet_setup()
                else:
                    print("Connection name must be alphanumeric")
                    ethernet_setup()
                os.system(
                    "nmcli connection add type ethernet ifname {} con-name {} ipv4.method manual ipv6.method disabled".format(
                        interface, connection_name))
                os.system("nmcli connection modify {} ipv4.addresses {} ipv4.method manual".format(connection_name,
                                                                                                   ip_address_netmask))
                os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                os.system("nmcli connection up {}".format(connection_name))
                ethernet_interfaces.remove(i)
                external_zone_interfaces.append(connection_name)
                internal_ip_subnets.append(ip_address_netmask)
            except os.error:
                print("Error creating connection")
                ethernet_setup()

        elif ask_ethernet == 'W' or ask_ethernet == 'w':
            try:
                # Set ethernet interface ipv4.method manual and ipv6.method disabled
                connection_name = input('Enter the connection name for interface {}: '.format(interface))
                if connection_name == '':
                    connection_name = interface
                elif connection_name.isalnum():
                    pass
                elif len(connection_name) < 7 or len(connection_name) > 15:
                    print("Connection name must be between 7 and 15 characters")
                    ethernet_setup()
                else:
                    print("Connection name must be alphanumeric")
                    ethernet_setup()
                # append slave to connection name
                connection_name = connection_name + ' slave'
                os.system(
                    "nmcli connection add type ethernet ifname {} con-name {} ipv4.method manual ipv6.method disabled".format(
                        interface, connection_name))
                os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                os.system("nmcli connection up {}".format(connection_name))
                ethernet_interfaces.remove(i)
                interfaces_for_bridge.append(interface)
            except os.error:
                print("Error creating connection")
                ethernet_setup()

        else:
            print("Invalid Input")
            ethernet_setup()


# Main Function
def main():
    # Get ethernet interfaces
    get_ethernet_interfaces()


# Run main function
if __name__ == '__main__':
    main()
