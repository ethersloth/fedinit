#!/bin/python3

import ipaddress
# Import modules
import os

import netifaces

user = ''

# Pull user variable from user.txt
def get_user():
    global user
    user = os.environ['user']


# Run cellular.py, ethernet.py, wifi.py, and bridge.py
os.system("python3 /home/{}/Desktop/workspace/Scripts/cellular.py".format(user))
os.system("python3 /home/{}/Desktop/workspace/Scripts/ethernet.py".format(user))
os.system("python3 /home/{}/Desktop/workspace/Scripts/wifi.py".format(user))
os.system("python3 /home/{}/Desktop/workspace/Scripts/bridge.py".format(user))

# variables
interfaces_for_bridge = []
internal_zone_interfaces = []
internal_ip_subnets = []
external_zone_interfaces = []
external_ip_subnets = []

# Get Hostname
def get_hostname():
    hostname = input("Enter the hostname: ")
    return hostname

# If hostname contains router run router_setup() else run firewall_setup()
def router_or_firewall():
    hostname = get_hostname()
    if "router" in hostname:
        router_setup()
    else:
        host_setup()

def router_setup():
    enable_ip_forwarding()
    setup_masquerade()
    setup_named_conf()
    setup_dhcp_server()
    setup_firewall()

def host_setup():
    # set all interfaces as external
    for interface in netifaces.interfaces():
        external_zone_interfaces.append(interface)
    setup_firewall()

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


# Setup Firewall
def setup_firewall():
    # Add zones
    os.system("firewall-cmd --permanent --new-zone=internal")
    os.system("firewall-cmd --permanent --new-zone=external")
    # Add interfaces to zones
    for i in internal_zone_interfaces:
        os.system("firewall-cmd --permanent --zone=internal --add-interface={}".format(i))
    for e in external_zone_interfaces:
        os.system("firewall-cmd --permanent --zone=external --add-interface={}".format(e))


# Main Function
def main():
    get_user()
    router_or_firewall()



# Run Main Function
if __name__ == "__main__":
    main()
