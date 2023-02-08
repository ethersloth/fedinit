#!/bin/python3

# Import modules
import os
import ipaddress
from firewall_setup import internal_ip_subnets, internal_zone_interfaces, interfaces_for_bridge

# variables


# Bridge Setup
def bridge_setup():
    # Ask the user if they want to create a bridge
    bridge_question = input('Do you want to create a bridge? (Y/N): ')
    if bridge_question == 'Y' or bridge_question == 'y':
        print(interfaces_for_bridge)
        # Ask the user to select the interfaces they want to add to the bridge from the interfaces_for_bridge list
        bridge_slave1 = input('Enter the first interface you want to add to the bridge: ')
        if bridge_slave1 in interfaces_for_bridge:
            pass
        else:
            print("Invalid interface")
            bridge_setup()
        bridge_slave2 = input('Enter the second interface you want to add to the bridge: ')
        if bridge_slave2 in interfaces_for_bridge:
            pass
        else:
            print("Invalid interface")
            bridge_setup()
        # Ask the user to enter the name of the bridge
        bridge_connection_name = input('Enter the name of the bridge: ')
        if bridge_connection_name == '':
            print("Invalid bridge name")
            bridge_setup()
        elif bridge_connection_name.isalnum():
            pass
        elif bridge_connection_name == 'lo':
            print("Invalid bridge name")
            bridge_setup()
        elif len(bridge_connection_name) < 1 or len(bridge_connection_name) > 15:
            print("Invalid bridge name")
            bridge_setup()
        else:
            print("Invalid bridge name")
            bridge_setup()
        # Ask the user for bridge interface name
        bridge_interface_name = input('Enter the name of the bridge interface, must be something like "br0": ')
        # bridge_interface_name must start with br and end with a number ex. br0
        if bridge_interface_name == '':
            bridge_interface_name = 'br0'
        elif bridge_interface_name.startswith('br') and bridge_interface_name[2:].isdigit():
            pass
        else:
            print("Invalid bridge interface name")
            bridge_setup()
        # Ask the user for bridge IP address and mask
        bridge_ip_and_mask = input(
            'Enter the IP address and mask for the bridge interface {}: '.format(bridge_interface_name))
        # Validate bridge_ip_and_mask with ipaddress module
        try:
            ipaddress.ip_network(bridge_ip_and_mask, strict=False)
        except ValueError:
            print("Invalid IP address and mask")
            bridge_setup()
        # Use nmcli to create bridge connection
        os.system(
            "nmcli connection add type bridge ifname {} con-name {} ipv4.method manual ipv4.addresses {} ipv6.method disabled".format(
                bridge_interface_name, bridge_connection_name, bridge_ip_and_mask))
        os.system("nmcli connection modify {} autoconnect yes".format(bridge_connection_name))
        os.system("nmcli connection up {}".format(bridge_connection_name))
        # Use nmcli to add bridge slaves
        os.system(
            "nmcli connection add type bridge-slave ifname {} master {}".format(bridge_slave1, bridge_connection_name))
        os.system(
            "nmcli connection add type bridge-slave ifname {} master {}".format(bridge_slave2, bridge_connection_name))
        # Remove the bridge slaves from the interfaces_for_bridge list
        interfaces_for_bridge.remove(bridge_slave1)
        interfaces_for_bridge.remove(bridge_slave2)
        # Add the bridge interface to the internal_ip_subnets list
        internal_ip_subnets.append(bridge_ip_and_mask)
        internal_zone_interfaces.append(bridge_interface_name)
        # Ask the user if they want to create another bridge
        bridge_question = input('Do you want to create another bridge? (Y/N): ')
        if bridge_question == 'Y' or bridge_question == 'y':
            bridge_setup()
        else:
            pass
    else:
        pass


# Main Function
def main():
    bridge_setup()


# Run main function
if __name__ == '__main__':
    main()
