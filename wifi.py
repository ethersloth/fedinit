#!/bin/python3
import ipaddress
import os
import getpass
import subprocess

from firewall_setup import internal_ip_subnets, internal_zone_interfaces, interfaces_for_bridge, \
    external_zone_interfaces

# Setup variables
valid_banda_channels = ['32', '34', '36', '38', '40', '42', '44', '46', '48', '149', '151', '153', '155', '157', '159',
                        '161', '165']
valid_bandbg_channels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
wifi_channel = []
wifi_interfaces = []


# Get Wifi Interfaces
def get_wifi_interfaces():
    global wifi_interfaces
    interfaces = subprocess.run(['nmcli', 'device', 'status'], capture_output=True, text=True).stdout
    if "wifi" in interfaces:
        for line in interfaces.splitlines():
            if "wifi" in line:
                wifi_interfaces.append(line.split()[0])
    else:
        print("No wifi interfaces found")
        return


# Setup wifi interfaces
def wifi_setup():
    if len(wifi_interfaces) < 1:
        pass
    global wifi_channel
    for interface in wifi_interfaces:
        # Ask if user wants to configure wifi interface as Bridge AP, AP, or Client
        ask_wifi = input(
            'Would you like to configure interface {} as Bridge AP, AP, or Client? (B/A/C): '.format(interface))
        if ask_wifi == 'B' or ask_wifi == 'b':
            try:
                # Set wifi interface ipv4.method manual and ipv6.method disabled
                connection_name = input('Enter the connection name for interface {}: '.format(interface))
                if connection_name == '':
                    connection_name = interface
                elif connection_name.isalnum():
                    pass
                elif len(connection_name) < 7 or len(connection_name) > 15:
                    print("Connection name must be between 7 and 15 characters")
                    wifi_setup()
                else:
                    print("Connection name must be alphanumeric")
                    wifi_setup()
                wifi_ssid = input('Enter the SSID for interface {}: '.format(interface))
                if wifi_ssid == '':
                    wifi_ssid = interface
                elif wifi_ssid.isalnum():
                    pass
                elif len(wifi_ssid) < 7 or len(wifi_ssid) > 15:
                    print("SSID must be between 7 and 15 characters")
                    wifi_setup()
                else:
                    print("SSID must be alphanumeric")
                    wifi_setup()
                # wifi password must be between 8 and 63 characters and masked
                wifi_password = getpass.getpass('Enter the password for interface {}: '.format(interface))
                if len(wifi_password) < 8 or len(wifi_password) > 63:
                    print("Password must be between 8 and 63 characters")
                    wifi_setup()
                elif wifi_password.isalnum():
                    pass
                else:
                    print("Password must be alphanumeric")
                    wifi_setup()
                # Ask user to select Wifi Band either a or bg
                wifi_band = input('Enter the Wifi Band for interface {} (a or bg): '.format(interface))
                if wifi_band == 'a':
                    wifi_band = 'a'
                elif wifi_band == 'bg':
                    wifi_band = 'bg'
                else:
                    print("Invalid Wifi Band")
                    wifi_setup()
                # Ask user to select Wifi Channel
                # If Wifi Band is a then channel must be in valid_banda_channels list
                # If Wifi Band is bg then channel must be in valid_bandbg_channels list
                wifi_channel = input('Enter the Wifi Channel for interface {}: '.format(interface))
                if wifi_band == 'a':
                    if wifi_channel in valid_banda_channels:
                        valid_banda_channels.remove(wifi_channel)
                        pass
                    else:
                        print("Invalid Wifi Channel")
                        wifi_setup()
                elif wifi_band == 'bg':
                    if wifi_channel in valid_bandbg_channels:
                        valid_bandbg_channels.remove(wifi_channel)
                        pass
                    else:
                        print("Invalid Wifi Channel")
                        wifi_setup()
                else:
                    print("Invalid Wifi Band")
                    wifi_setup()
                # append slave to connection name
                connection_name = connection_name + ' slave'
                os.system(
                    "nmcli connection add type wifi ifname {} con-name {} ssid {} wifi-sec.key-mgmt wpa-psk wifi-sec.psk {} 802-11-wireless.mode ap 802-11-wireless.band {} 802-11-wireless.channel {} ipv4.method shared ipv6.method disabled".format(
                        interface, connection_name, wifi_ssid, wifi_password, wifi_band, wifi_channel))
                os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                os.system("nmcli connection up {}".format(connection_name))
                wifi_interfaces.remove(interface)
                interfaces_for_bridge.append(interface)
            except os.error:
                print("Error creating connection")
                wifi_setup()
        elif ask_wifi == 'A' or ask_wifi == 'a':
            try:
                # Set wifi interface ipv4.method manual and ipv6.method disabled
                connection_name = input('Enter the connection name for interface {}: '.format(interface))
                if connection_name == '':
                    connection_name = interface
                elif connection_name.isalnum():
                    pass
                elif len(connection_name) < 7 or len(connection_name) > 15:
                    print("Connection name must be between 7 and 15 characters")
                    wifi_setup()
                else:
                    print("Connection name must be alphanumeric")
                    wifi_setup()
                wifi_ssid = input('Enter the SSID for interface {}: '.format(interface))
                if wifi_ssid == '':
                    wifi_ssid = interface
                elif wifi_ssid.isalnum():
                    pass
                elif len(wifi_ssid) < 7 or len(wifi_ssid) > 15:
                    print("SSID must be between 7 and 15 characters")
                    wifi_setup()
                else:
                    print("SSID must be alphanumeric")
                    wifi_setup()
                # wifi password must be between 8 and 63 characters and masked
                wifi_password = getpass.getpass('Enter the password for interface {}: '.format(interface))
                if len(wifi_password) < 8 or len(wifi_password) > 63:
                    print("Password must be between 8 and 63 characters")
                    wifi_setup()
                elif wifi_password.isalnum():
                    pass
                else:
                    print("Password must be alphanumeric")
                    wifi_setup()
                # Ask user to select Wifi Band either a or bg
                wifi_band = input('Enter the Wifi Band for interface {} (a or bg): '.format(interface))
                if wifi_band == 'a':
                    wifi_band = 'a'
                elif wifi_band == 'bg':
                    wifi_band = 'bg'
                else:
                    print("Invalid Wifi Band")
                    wifi_setup()
                # Ask user to select Wifi Channel
                # If Wifi Band is a then channel must be in valid_banda_channels list
                # If Wifi Band is bg then channel must be in valid_bandbg_channels list
                wifi_channel = input('Enter the Wifi Channel for interface {}: '.format(interface))
                if wifi_band == 'a':
                    if wifi_channel in valid_banda_channels:
                        valid_banda_channels.remove(wifi_channel)
                        pass
                    else:
                        print("Invalid Wifi Channel")
                        wifi_setup()
                elif wifi_band == 'bg':
                    if wifi_channel in valid_bandbg_channels:
                        valid_bandbg_channels.remove(wifi_channel)
                        pass
                    else:
                        print("Invalid Wifi Channel")
                        wifi_setup()
                else:
                    print("Invalid Wifi Band")
                    wifi_setup()
                wifi_ip_and_mask = input('Enter the IP address and mask for interface {}: '.format(interface))
                if wifi_ip_and_mask == '':
                    wifi_ip_and_mask = '192.168.255.1/24'
                    # validate with ipaddress module
                    try:
                        ipaddress.ip_network(wifi_ip_and_mask, strict=False)
                    except ValueError:
                        print("Invalid IP address and mask")
                        wifi_setup()
                else:
                    # validate with ipaddress module
                    try:
                        ipaddress.ip_network(wifi_ip_and_mask, strict=False)
                    except ValueError:
                        print("Invalid IP address and mask")
                        wifi_setup()
                # use nmcli to create wifi connection
                os.system(
                    "nmcli connection add type wifi ifname {} con-name {} ssid {} wifi-sec.key-mgmt wpa-psk wifi-sec.psk {} 802-11-wireless.mode ap 802-11-wireless.band {} 802-11-wireless.channel {} ipv4.method manual ipv4.addresses {} ipv6.method disabled".format(
                        interface, connection_name, wifi_ssid, wifi_password, wifi_band, wifi_channel,
                        wifi_ip_and_mask))
                os.system("nmcli connection modify {} autoconnect yes".format(connection_name))
                os.system("nmcli connection up {}".format(connection_name))
                wifi_interfaces.remove(interface)
                internal_zone_interfaces.append(interface)
                internal_ip_subnets.append(wifi_ip_and_mask)
            except os.error:
                print("Error creating connection")
                wifi_setup()
        elif ask_wifi == 'C' or ask_wifi == 'c':
            try:
                # Use nmcli to list wifi access points and show them to the user in a numbered list
                # User selects the access point they want to connect to
                # User enters the password for the access point
                # Use nmcli to create wifi connection
                wifi_ap_list = os.popen("nmcli device wifi list").read()
                for i, line in enumerate(wifi_ap_list.splitlines()):
                    print(i, line)
                wifi_ap = input('Enter the number of the access point you want to connect to: ')
                wifi_ap = int(wifi_ap)
                if wifi_ap in range(0, len(wifi_ap_list)):
                    pass
                else:
                    print("Invalid access point")
                    wifi_setup()
                wifi_password = getpass.getpass('Enter the password for interface {}: '.format(interface))
                if len(wifi_password) < 8 or len(wifi_password) > 63:
                    print("Password must be between 8 and 63 characters")
                    wifi_setup()
                elif wifi_password.isalnum():
                    pass
                else:
                    print("Password must be alphanumeric")
                    wifi_setup()
                os.system("nmcli device wifi connect {} password {}".format(wifi_ap_list[wifi_ap], wifi_password))
                wifi_interfaces.remove(interface)
                external_zone_interfaces.append(interface)
                # Get the IP address and mask for the interface append to internal_ip_subnets list
                ip_subnet = os.popen("ip addr show {}".format(interface)).read()
                ip_subnet = ip_subnet.splitlines()[2].split()[1]
                internal_ip_subnets.append(ip_subnet)
            except os.error:
                print("Error connecting to access point")
                wifi_setup()
        else:
            print("Invalid selection")
            wifi_setup()
    else:
        pass


# Main function
def main():
    get_wifi_interfaces()
    wifi_setup()


if __name__ == '__main__':
    main()
