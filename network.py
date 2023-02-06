#!/bin/python3
import getpass
import ipaddress
import os
import subprocess

from fedinitinstall import new_user

# This script is for setting up Network Interfaces on Linux
wifi_interfaces = []
ethernet_interfaces = []
cdc_wdm_interfaces = []
interfaces_for_bridge = []
interfaces_for_bond = []
bridge_interfaces = []
valid_banda_channels = ['32', '34', '36', '38', '40', '42', '44', '46', '48', '149', '151', '153', '155', '157', '159',
                        '161', '165']
valid_bandbg_channels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
wifi_channel = []
internal_ip_subnets = []
internal_zone_interfaces = []
external_zone_interfaces = []
failover_priority = []


# Using nmcli list all the network interfaces
def list_interfaces():
    interfaces = os.popen("nmcli device status").read()
    # filter out un-editable interfaces
    interfaces = interfaces.splitlines()
    for i in interfaces:
        if 'lo' in i:
            interfaces.remove(i)
        elif 'tun' in i:
            interfaces.remove(i)
        elif 'tap' in i:
            interfaces.remove(i)
        elif 'ipsec' in i:
            interfaces.remove(i)
        else:
            pass
    for i in interfaces:
        if 'ethernet' in i:
            ethernet_interfaces.append(i)
        elif 'wifi' in i:
            wifi_interfaces.append(i)
        else:
            pass
    cdc_wdm()
    print("Ethernet Interfaces: " + str(ethernet_interfaces))
    print("Wifi Interfaces: " + str(wifi_interfaces))
    print("Cellular Interfaces: " + str(cdc_wdm_interfaces))


# Look for cdc-wdm* in nmcli device status
def cdc_wdm():
    cellular_setup()
    interfaces = os.popen("nmcli device status").read()
    interfaces = interfaces.splitlines()
    for i in interfaces:
        if 'cdc-wdm' in i:
            cdc_wdm_interfaces.append(i)
        else:
            pass


# Make sure all valid connection are managed by NetworkManager
def nmcli_manage():
    for i in ethernet_interfaces:
        os.system("nmcli device set " + i + " managed yes")
    for i in wifi_interfaces:
        os.system("nmcli device set " + i + " managed yes")
    for i in cdc_wdm_interfaces:
        os.system("nmcli device set " + i + " managed yes")


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
                cellular_setup()
    ethernet_setup()


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
                ethernet_interfaces.remove(i)
                external_zone_interfaces.append(connection_name)
                wifi_setup()
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
                wifi_setup()
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
                wifi_setup()
            except os.error:
                print("Error creating connection")
                ethernet_setup()


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
                bridge_setup()
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
                bridge_setup()
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
                bridge_setup()
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


# Using the external_zone_interfaces list, ask user to select each interface in order of failover priority, append to failover_priority list
def set_failover_priority():
    if len(external_zone_interfaces) < 1:
        pass
    else:
        print(external_zone_interfaces)
        failover = input(
            'Enter the interface {} in order of failover priority: (First entry will have highest priority, Last entry will have lowest. ')
        if failover in external_zone_interfaces:
            failover_priority.append(failover)
            external_zone_interfaces.remove(failover)
            if len(external_zone_interfaces) > 0:
                set_failover_priority()
            else:
                print("Failover priority set")
        else:
            print("Invalid interface")
            set_failover_priority()
        print(failover_priority)
    ask_confirm_priority = input('Are you satisfied with the failover priority? (Y/N): If not we will start over. ')
    if ask_confirm_priority == 'Y' or ask_confirm_priority == 'y':
        set_wan_failover_service()
    else:
        failover_priority.clear()
        set_failover_priority()


# Set the wan failover.py script as a service that runs on boot
def set_wan_failover_service():
    user = new_user()
    os.system("cp /home/{}/wan_failover.py /etc/wan_failover.py".format(user))
    os.system("chmod +x /etc/wan_failover.py")
    os.system("chown root:root /etc/wan_failover.py")
    os.system("chmod 755 /etc/wan_failover.py")
    create_wan_failover_service()


# Create a service file for the wan failover.py script
def create_wan_failover_service():
    os.system("touch /etc/systemd/system/wan_failover.service")
    os.system("echo '[Unit]' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'Description=wan_failover' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'After=network.target' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '[Service]' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'Type=simple' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'ExecStart=/usr/bin/python3 /etc/wan_failover.py' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '[Install]' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'WantedBy=multi-user.target' >> /etc/systemd/system/wan_failover.service")
    os.system("systemctl daemon-reload")
    os.system("systemctl enable wan_failover.service")
    os.system("systemctl start wan_failover.service")


# Remove all but Internal and External Zones from firewalld
def remove_all_zones():
    zone = subprocess.check_output("ls -al /etc/firewalld/zones", shell=True)
    zone = zone.decode('utf-8')
    zone = zone.split()
    for i in zone:
        if i.startswith('internal') or i.startswith('external'):
            pass
        else:
            os.system("rm /etc/firewalld/zones/{}.xml".format(i))
            os.system("firewall-cmd --permanent --remove-zone={}".format(i))
            os.system("firewall-cmd --reload")
    zone = subprocess.check_output("ls -al /usr/lib/firewalld/zones/", shell=True)
    zone = zone.decode('utf-8')
    zone = zone.split()
    for i in zone:
        if i.startswith('internal') or i.startswith('external'):
            pass
        else:
            os.system("rm /usr/lib/firewalld/zones/{}.xml".format(i))
            os.system("firewall-cmd --permanent --remove-zone={}".format(i))
            os.system("firewall-cmd --reload")
    setup_internal_zone()


# Setup the Internal Zone as Default Zone in firewalld, add all interfaces in internal_zone_interfaces to the internal zone
def setup_internal_zone():
    os.system("firewall-cmd --permanent --new-zone=internal")
    for i in internal_zone_interfaces:
        # Create a new zone for internal interfaces
        os.system("firewall-cmd --permanent --zone=internal --add-interface={}".format(i))
        os.system("firewall-cmd --reload")
    setup_external_zone()


# Setup external zone, add all interfaces in external_zone_interfaces to the external zone
def setup_external_zone():
    os.system("firewall-cmd --permanent --new-zone=external")
    os.system("firewall-cmd --set-default-zone=external")
    for i in external_zone_interfaces:
        os.system("firewall-cmd --permanent --zone=external --add-interface={}".format(i))
        os.system("firewall-cmd --reload")
    enable_ip_forwarding()


# Enable IP Forwarding
def enable_ip_forwarding():
    os.system("echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf")
    os.system("sysctl -p")
    os.system("sysctl -w net.ipv4.ip_forward=1")
    setup_masquerade()


# Setup MASQUERADE and Filter Forwarding
def setup_masquerade():
    for e in external_zone_interfaces:
        for i in internal_zone_interfaces:
            os.system(
                "firewall-cmd --permanent --direct --add-rule ipv4 nat POSTROUTING 0 -o {} -j MASQUERADE".format(e))
            os.system(
                "firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i {} -o {} -j ACCEPT".format(i, e))
            os.system(
                "firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i {} -o {} -m state --state RELATED,ESTABLISHED -j ACCEPT".format(
                    e, i))
            os.system("firewall-cmd --reload")
    setup_named_conf()


# Setup named.conf
def setup_named_conf():
    os.system("systemctl stop named")
    os.system("rm /etc/named.conf")
    os.system("touch /etc/named.conf")
    os.system("echo 'options {' >> /etc/named.conf")
    # For every subnet in internal_subnets, add a listen-on
    # Using the ipaddress module to get the first ip address in the subnet
    for i in internal_ip_subnets:
        ip = ipaddress.ip_network(i)
        ip = ip[1]
        os.system("echo 'listen-on port 53 {{ {} }};' >> /etc/named.conf".format(ip))
    # For every subnet in internal_subnets, add a allow-query
    for i in internal_ip_subnets:
        os.system("echo 'allow-query {{ {} }};' >> /etc/named.conf".format(i))
    # add an allow-recursion
    for i in internal_ip_subnets:
        os.system("echo 'allow-recursion {{ {} }};' >> /etc/named.conf".format(i))
    # append localhost to allow query line
    os.system("echo 'allow-query {{ localhost; }};' >> /etc/named.conf")
    # append localhost to allow recursion line
    os.system("echo 'allow-recursion {{ localhost; }};' >> /etc/named.conf")
    # append 127.0.0.1 to listen on line
    os.system("echo 'listen-on port 53 {{ 127.0.0.1; }};' >> /etc/named.conf")
    # append forwarders
    forwarders = "8.8.8.8", "8.8.4.4"
    for i in forwarders:
        os.system("echo 'forwarders {{ {} }};' >> /etc/named.conf".format(i))
    # append recursion yes
    os.system("echo 'recursion yes;' >> /etc/named.conf")
    # append forward only
    os.system("echo 'forward only;' >> /etc/named.conf")
    # close options
    os.system("echo '};' >> /etc/named.conf")
    # Restart named
    os.system("systemctl start named")
    os.system("systemctl enable named")
    setup_dhcp_server()


# Setup DHCP Server
def setup_dhcp_server():
    os.system("systemctl stop dhcpd")
    os.system("rm /etc/dhcp/dhcpd.conf")
    os.system("touch /etc/dhcp/dhcpd.conf")
    # Using the ipaddress module to get the first ip and last ip in the subnet
    for i in internal_ip_subnets:
        ip = ipaddress.ip_network(i)
        ip_first = ip[1]
        ip_last = ip[-1]
        os.system("echo 'subnet {} netmask {} {{' >> /etc/dhcp/dhcpd.conf".format(ip_first, ip.netmask))
        os.system("echo 'range {} {};' >> /etc/dhcp/dhcpd.conf".format(ip_first, ip_last))
        os.system("echo 'option routers {};' >> /etc/dhcp/dhcpd.conf".format(ip_first))
        os.system("echo 'option domain-name-servers {};' >> /etc/dhcp/dhcpd.conf".format(ip_first))
        os.system("echo '}}' >> /etc/dhcp/dhcpd.conf")
    # Restart dhcpd
    os.system("systemctl start dhcpd")
    os.system("systemctl enable dhcpd")


# Main Function
def main():
    list_interfaces()
    nmcli_manage()
    cellular_setup()
    ethernet_setup()
    wifi_setup()
    set_failover_priority()
    remove_all_zones()


# Run Main Function
if __name__ == "__main__":
    main()
