#!/bin/python3
import datetime
import json
import os
import platform
import re
import socket
import uuid

import dropbox
import psutil
from fedinitinstall import user

hostname = ""

# system_config_json template
# {
#     "system_config": {
#         "system_name": "systemname",
#         "system_type": "systemtype",
#         "system_hostname": "hostname",
#         "system_domain": "domain",
#         "system_cpu": "cpu",
#         "system_memory": "memory",
#         "system_kernel": "kernel",
#         "system_os": "os",
#         "system_architecture": "architecture",
#         "system_uptime": "uptime",
#         "system_last_boot": "lastboot",
#         "system_last_update": "lastupdate",
#         "system_last_reboot": "lastreboot",
#         "system_last_shutdown": "lastshutdown",
#         "system_last_crash": "last crash",
#         "system_last_login": "lastlogin",
#         "system_last_logout": "lastlogout",
#         "system_last_user": "lastuser",
#         }

#         "system_interfaces": {
#             for interface in interfaces:
#                 "interface_name": "interface",
#                 "interface_ip": "ip",
#                 "interface_netmask": "netmask",
#                 "interface_gateway": "gateway",
#                 "interface_dns": "dns",
#                 "interface_mac": "mac",
#                 "interface_type": "type"
#                   }
#         "system_routes": {
#             "route_name": "route",
#             "route_gateway": "gateway",
#             "route_netmask": "netmask",
#             "route_interface": "interface"
#         }
#         "system_arp_table": {
#             "arp_name": "arp",
#             "arp_ip": "ip",
#             "arp_mac": "mac",
#             "arp_interface": "interface"
#         }
#         "system_netstat": {
#             "netstat_name": "netstat",
#             "netstat_protocol": "protocol",
#             "netstat_local_address": "local_address",
#             "netstat_foreign_address": "foreign_address",
#             "netstat_state": "state",
#             "netstat_pid": "pid"
#         }
#         if dhcpd is installed:
#             "system_dhcpd": {
#                 "dhcpd_name": "dhcpd",
#                 "dhcpd_subnet": "subnet",
#                 "dhcpd_netmask": "netmask",
#                 "dhcpd_range": "range",
#                 "dhcpd_broadcast": "broadcast",
#                 "dhcpd_routers": "routers",
#                 "dhcpd_domain_name_servers": "domain_name_servers",
#                 "dhcpd_domain_name": "domain_name",
#                 "dhcpd_default_lease_time": "default_lease_time",
#                 "dhcpd_max_lease_time": "max_lease_time",
#                 "dhcpd_authoritative": "authoritative",
#                 "dhcpd_log_facility": "log_facility",
#         }
#         "system_time": {
#             "time_zone": "timezone",
#             "time_server": "timeserver"
#         }
#         "system_users": {
#             "user_name": "user",
#             "user_password": "password",
#             "user_groups": "groups"
#         }
#         "system_services": {
#             "service_name": "service",
#             "service_status": "status"
#         }
#         "system_packages": {
#             "package_name": "package",
#             "package_status": "status"
#         }
#         "system_firewall_zones": {
#             "zone_name": "zone",
#             "zone_interfaces": "interfaces",
#             "zone_services": "services",
#             "zone_ports": "ports",
#             "zone_protocols": "protocols",
#             "zone_source_addresses": "source_addresses",
#             "zone_destination_addresses": "destination_addresses",
#             "zone_masquerade": "masquerade",
#             "zone_forward_ports": "forward_ports",
#             "zone_icmp_block": "icmp_block",
#             "zone_icmp_block_inversion": "icmp_block_inversion",
#             "zone_target": "target"
#         }
#         "system_fstab": {
#             "fstab_name": "fstab",
#             "fstab_device": "device",
#             "fstab_mount_point": "mount_point",
#             "fstab_file_system_type": "file_system_type",
#             "fstab_mount_options": "mount_options",
#             "fstab_dump": "dump",
#             "fstab_pass": "pass"
#         }
#         "system_disks": {
#             "disk_name": "disk",
#             "disk_size": "size",
#             "disk_type": "type",
#             "disk_file_system": "file_system",
#             "disk_mount_point": "mount_point"
#         }
#         "system_theme": {
#             "theme_application_style": "application_style",
#             "theme_plasma_style": "plasma_style",
#             "theme_color_scheme": "color_scheme",
#             "theme_window_decoration": "window_decoration",
#             "theme_font": "font",
#             "theme_icons": "icons",
#             "theme_cursor": "cursor",
#             "theme_wallpaper": "wallpaper"
#             "theme_splash_screen": "splash_screen"
#         }
#         "system_cellular_config": {
#             "cellular_name": "cellular",
#             "cellular_apn": "apn",
#             "cellular_username": "username",
#             "cellular_password": "password",
#             "cellular_pin": "pin"
#             "cellular_csq": "csq"
#         }
#         "system_gps_config": {
#             "gps_name": "gps",
#             "gps_device": "device",
#             "gps_baud_rate": "baud_rate",
#             "gps_data_bits": "data_bits",
#             "gps_parity": "parity",
#             "gps_stop_bits": "stop_bits",
#             "gps_flow_control": "flow_control"
#             "gps_location": "location"
#         }
#         "system_systemd_config": {
#             "systemd_name": "systemd",
#             "systemd_unit": "unit",
#             "systemd_status": "status"
#         }
#         "system_vnstat_config": {
#             "vnstat_name": "vnstat",
#             "vnstat_interface": "interface",
#             "vnstat_rx": "rx",
#             "vnstat_tx": "tx"
#         }
#     }
# }


# Create Function to get the system information
def get_system_info():
    # Get the hostname
    global hostname
    hostname = socket.gethostname()
    # Get the IP address
    ip = socket.gethostbyname(hostname)
    # Get the MAC address
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    # Get the system type
    os_type = platform.system()
    # Get the system release
    release = platform.release()
    # Get the system version
    version = platform.version()
    # Get the system architecture
    architecture = platform.machine()
    # Get the system processor
    processor = platform.processor()
    # Get the system uptime
    datetime.datetime.now()
    uptime = datetime.datetime.fromtimestamp(psutil.boot_time())
    # Get the system load
    load = psutil.getloadavg()
    # Get the system memory
    memory = psutil.virtual_memory()
    # Get the system swap
    swap = psutil.swap_memory()
    # Get the system disk
    disk = psutil.disk_usage('/')
    # Get the system network
    network = psutil.net_if_addrs()
    # Get the system routes
    routes = psutil.net_if_addrs()
    # Get the system arp table
    arp_table = psutil.net_if_addrs()
    # Get the system netstat
    netstat = psutil.net_connections()
    # Get the system time
    time = datetime.datetime.now()
    # Get the system users
    users = psutil.users()
    # Get the system services
    services = psutil.pids()
    # Get the system packages
    packages = psutil.pids()
    # Get the system firewall zones
    firewall_zones = psutil.pids()
    # Get the system fstab
    fstab = psutil.pids()
    # Get the system disks
    disks = psutil.disk_partitions()
    # Get the system theme
    theme = psutil.pids()
    # Get the system cellular config
    cellular_config = psutil.pids()
    # Get the system gps config
    gps_config = psutil.pids()
    # Get the system systemd config
    systemd_config = psutil.pids()
    # Get the system vnstat config
    vnstat_config = psutil.pids()

    # Create the system information dictionary
    system_info = {
        "hostname": hostname,
        "ip": ip,
        "mac": mac,
        "type": os_type,
        "release": release,
        "version": version,
        "architecture": architecture,
        "processor": processor,
        "uptime": uptime,
        "load": load,
        "memory": memory,
        "swap": swap,
        "disk": disk,
        "network": network,
        "routes": routes,
        "arp_table": arp_table,
        "netstat": netstat,
        "time": time,
        "users": users,
        "services": services,
        "packages": packages,
        "firewall_zones": firewall_zones,
        "fstab": fstab,
        "disks": disks,
        "theme": theme,
        "cellular_config": cellular_config,
        "gps_config": gps_config,
        "systemd_config": systemd_config,
        "vnstat_config": vnstat_config
    }

    # Return the system information dictionary
    return system_info


# Create Function to convert the system information dictionary to JSON using the template and json.dumps
def convert_system_info_to_json(system_info):
    # Create the JSON string
    json_string = json.dumps(system_info, indent=4, sort_keys=True)

    # Return the JSON string
    return json_string


# Create Function to write the JSON string to a file
def write_json_to_file(json_string):
    # Open the file
    with open("system_info.json", "w") as file:
        # Write the JSON string to the file
        file.write(json_string)


# Create function to get last 10000 lines of journalctl to a file and put in /workspace/logs folder
def get_journalctl():
    # Get the last 10000 lines of journalctl
    os.system("journalctl -n 10000 > /workspace/logs/journalctl.log")


# If IPSec VPN is enabled, get the IPsec VPN config and put in /workspace/logs folder
def get_ipsec_vpn_config():
    if os.path.exists("/etc/ipsec.conf"):
        os.system("cp /etc/ipsec.conf /workspace/logs/ipsec.conf")
    if os.path.exists("/etc/ipsec.secrets"):
        os.system("cp /etc/ipsec.secrets /workspace/logs/ipsec.secrets")


# If OpenVPN is enabled, get the OpenVPN config and put in /workspace/logs folder
def get_openvpn_config():
    if os.path.exists("/etc/openvpn/server/" + os.listdir("/etc/openvpn/server")[0]):
        os.system("cp /etc/openvpn/server/" + os.listdir("/etc/openvpn/server")[0] + " /home/{}/Desktop/workspace/logs/openvpn/".format(user) + os.listdir("/etc/openvpn/server")[0])
    elif os.path.exists("/etc/openvpn/client/" + os.listdir("/etc/openvpn/client")[0]):
        os.system("cp /etc/openvpn/client/" + os.listdir("/etc/openvpn/client")[0] + " /home/{}/Desktop/workspace/logs/openvpn/".format(user) + os.listdir("/etc/openvpn/client")[0])
    else:
        print("OpenVPN not found")


# Zip up the logs folder and system_info.json file and put in /workspace folder
def zip_logs():
    os.system("zip -r /home/{}/Desktop/workspace/system_config.zip /home/{}/Desktop/workspace/logs".format(user, user))
    # add system_info.json to the zip file
    os.system("zip -ur /home/{}/Desktop/workspace/system_config.zip /home/{}/Desktop/workspace/system_info.json".format(user, user))
    # append hostname to the zip file name
    os.system("mv /home/{}/Desktop/workspace/system_config.zip /home/{}/Desktop/workspace/system_config_{}.zip".format(user, user, hostname))


# Create Function to send the zip file to dropbox
def send_to_dropbox():
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
    )
    # Upload the zip file to dropbox
    with open("/home/{}/Desktop/workspace/system_config_{}.zip".format(user, hostname), "rb") as f:
        dbx.files_upload(f.read(), "/system_config_{}.zip".format(hostname), mute=True)


# Create main function
def main():
    # Get the system information
    system_info = get_system_info()
    # Convert the system information dictionary to JSON
    json_string = convert_system_info_to_json(system_info)
    # Write the JSON string to a file
    write_json_to_file(json_string)
    # Get the last 10000 lines of journalctl
    get_journalctl()
    # If IPSec VPN is enabled, get the IPsec VPN config
    get_ipsec_vpn_config()
    # If OpenVPN is enabled, get the OpenVPN config
    get_openvpn_config()
    # Zip up the logs folder and system_info.json file
    zip_logs()
    # Send the zip file to dropbox
    send_to_dropbox()


# Run the main function
if __name__ == "__main__":
    main()
