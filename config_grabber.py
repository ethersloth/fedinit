#!/bin/python3
from datetime import datetime
import dropbox
import os
import socket

hostname = ''


# Create a directory to store all the config files
def create_workspace_system_config():
    os.system('mkdir /home/gwhitlock/Desktop/workspace')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/openvpn')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/ipsec')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/wireguard')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/config_scripts')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/dhcpd')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/firewalld')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/fstab')
    os.system('mkdir /home/gwhitlock/Desktop/workspace/system_config/network_interfaces')


def zsh_history():
    os.system('cat /root/.zsh_history >> /home/gwhitlock/Desktop/workspace/system_config/zsh_history.txt')
    os.system('cat /home/gwhitlock/.zsh_history >> /home/gwhitlock/Desktop/workspace/system_config/zsh_history.txt')


# Grab OS, OS Version, and Kernel Version to a json file named system_config.json
def system_config():
    os.system('cat /etc/os-release > /home/gwhitlock/Desktop/workspace/system_config/system_config.json')
    os.system('uname -a >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# Grab CPU Info and append to system_config.json
def cpu_info():
    os.system('cat /proc/cpuinfo >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# Grab Memory Info and append to system_config.json
def memory_info():
    os.system('cat /proc/meminfo >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# Grab Disk Info and append to system_config.json
def disk_info():
    os.system('df -h >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# Grab fstab and append to a file named fstab.txt
def fstab():
    os.system('cat /etc/fstab >> /home/gwhitlock/Desktop/workspace/system_config/fstab/fstab.txt')


# Grab Running Processes and append to system_config.json
def running_processes():
    os.system('ps -aux >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# Grab Current System Time and UpTime and append to system_config.json
def system_time():
    os.system('date >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')
    os.system('uptime >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# If GPS is enabled, grab GPS data and append to system_config.json
def gps_data():
    os.system('cat /var/log/gpsd.log >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


# Grab All Network Interfaces and IP Addresses and append to system_config.json
def network_interfaces():
    os.system('ip a >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')
    interfaces = os.listdir('/etc/NetworkManager/system-connections/')
    for interface in interfaces:
        os.system(
            'cp -air /etc/NetworkManager/system-connections/' + interface + ' /home/gwhitlock/Desktop/workspace/system_config/network_interfaces/' + interface)


# Grab All OpenVPN Server configs and copy to this directory
def openvpn_server_configs():
    os.system('cp /etc/openvpn/server/*.conf /home/gwhitlock/Desktop/workspace/system_config/openvpn/server/*.conf')
    os.system('cp /etc/openvpn/server/*.ovpn /home/gwhitlock/Desktop/workspace/system_config/openvpn/server/*.ovpn')


# Grab All OpenVPN Client configs and copy to this directory
def openvpn_client_configs():
    os.system('cp /etc/openvpn/client/*.conf /home/gwhitlock/Desktop/workspace/system_config/openvpn/client/*.conf')
    os.system('cp /etc/openvpn/client/*.ovpn /home/gwhitlock/Desktop/workspace/system_config/openvpn/client/*.ovpn')


# Grab All IPSec configs and copy to this directory
def ipsec_configs():
    os.system('cp /etc/ipsec.d/*.conf /home/gwhitlock/Desktop/workspace/system_config/ipsec/*.conf')
    os.system('cp /etc/ipsec.d/*.secrets /home/gwhitlock/Desktop/workspace/system_config/ipsec/*.secrets')


# Grab All WireGuard configs and copy to this directory
def wireguard_configs():
    os.system('cp /etc/wireguard/*.conf /home/gwhitlock/Desktop/workspace/system_config/wireguard/*.conf')
    os.system('cp /etc/wireguard/*.key /home/gwhitlock/Desktop/workspace/system_config/wireguard/*.key')


# Grab All DHCPD configs and copy to this directory
def dhcpd_configs():
    os.system('cp /etc/dhcpd.conf /home/gwhitlock/Desktop/workspace/system_config/dhcpd/dhcpd.conf')
    os.system('cp /etc/dhcpd/dhcpd.conf /home/gwhitlock/Desktop/workspace/system_config/dhcpd/dhcpd.conf')


# Grab All of FirewallD configs and copy to this directory
def firewalld_configs():
    os.system('cp /etc/firewalld/*.xml /home/gwhitlock/Desktop/workspace/system_config/firewalld/*.xml')
    os.system('cp /etc/firewalld/*.xml /home/gwhitlock/Desktop/workspace/system_config/firewalld/*.xml')


# Zip All Folders and Files in the workspace/system_config directory
def zip_system_config():
    os.system(
        'zip -r /home/gwhitlock/Desktop/workspace/system_config.zip /home/gwhitlock/Desktop/workspace/system_config')


# Change the name of the zip file to the hostname of the system and append the date and time
def rename_system_config_zip():
    global hostname
    hostname = socket.gethostname()
    date_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    os.system(
        'mv /home/gwhitlock/Desktop/workspace/system_config.zip /home/gwhitlock/Desktop/workspace/' + hostname + '_' + date_time + '.zip')


# Send the zip file to Dropbox
def send_system_config_zip():
    global hostname
    hostname = socket.gethostname()
    date_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    dbx = dropbox.Dropbox(
        'sl.BX3VVSTTHKAg2tQvY5LLIEbgtwW29pRUaQl6KbgklwKQI98ZWt2UPXXFLhstXSPYDZJQcB0L9jHlS-FwAZk7ybl0JPeUT1w8zcKqzZAwBcf0TRtPBZcARLaVzRtwJ4HJNiMeb9g')
    with open('/home/gwhitlock/Desktop/workspace/' + hostname + '_' + date_time + '.zip', 'rb') as f:
        dbx.files_upload(f.read(), '/' + hostname + '_' + date_time + '.zip', mode=dropbox.files.WriteMode.overwrite)


# Run all functions
def get_hostname():
    global hostname
    os.system('{} >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json'.format('hostname'))


def os_version():
    os.system('cat /etc/os-release >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


def kernel_version():
    os.system('uname -a >> /home/gwhitlock/Desktop/workspace/system_config/system_config.json')


def main():
    get_hostname()
    os_version()
    kernel_version()
    cpu_info()
    memory_info()
    disk_info()
    fstab()
    running_processes()
    system_time()
    gps_data()
    network_interfaces()
    openvpn_server_configs()
    openvpn_client_configs()
    ipsec_configs()
    wireguard_configs()
    dhcpd_configs()
    firewalld_configs()
    zip_system_config()
    rename_system_config_zip()
    send_system_config_zip()


if __name__ == '__main__':
    main()
