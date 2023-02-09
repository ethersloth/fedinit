#!/bin/python3
import os
import pwd
import socket
import subprocess
import json
import dropbox
import psutil
from netifaces import interfaces

from fedinitinstall import user


# Variables
def get_hostname():
    hostname = socket.gethostname()
    return hostname


# Create Function to get the system information
def get_system_theme_info():
    #   "theme_application_style": "application_style",
    #   "theme_plasma_style": "plasma_style",
    #   "theme_color_scheme": "color_scheme",
    #   "theme_window_decoration": "window_decoration",
    #   "theme_font": "font",
    #   "theme_icons": "icons",
    #   "theme_cursor": "cursor",
    #   "theme_wallpaper": "wallpaper"
    #   "theme_splash_screen": "splash_screen"
    #   "theme_login_screen": "login_screen"
    #   "theme_lock_screen": "lock_screen"
    #   "theme_global_theme": "global_theme"

    application_style = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                       capture_output=True, text=True).stdout.strip()
    plasma_style = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                  capture_output=True, text=True).stdout.strip()
    color_scheme = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key ColorScheme"],
                                  capture_output=True, text=True).stdout.strip()
    window_decoration = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                       capture_output=True, text=True).stdout.strip()
    font = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"], capture_output=True,
                          text=True).stdout.strip()
    icons = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"], capture_output=True,
                           text=True).stdout.strip()
    cursor = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"], capture_output=True,
                            text=True).stdout.strip()
    wallpaper = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                               capture_output=True, text=True).stdout.strip()
    splash_screen = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                   capture_output=True, text=True).stdout.strip()
    login_screen = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                  capture_output=True, text=True).stdout.strip()
    lock_screen = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                 capture_output=True, text=True).stdout.strip()
    global_theme = subprocess.run(["kreadconfig5 --file kdeglobals --group General --key widgetStyle"],
                                  capture_output=True, text=True).stdout.strip()

    return {
        "theme_application_style": application_style,
        "theme_plasma_style": plasma_style,
        "theme_color_scheme": color_scheme,
        "theme_window_decoration": window_decoration,
        "theme_font": font,
        "theme_icons": icons,
        "theme_cursor": cursor,
        "theme_wallpaper": wallpaper,
        "theme_splash_screen": splash_screen,
        "theme_login_screen": login_screen,
        "theme_lock_screen": lock_screen,
        "theme_global_theme": global_theme
    }


def get_cpu_info():
    #   "cpu_model": "model",
    #   "cpu_cores": "cores",
    #   "cpu_threads": "threads",
    #   "cpu_frequency": "frequency",
    #   "cpu_usage": "usage",
    #   "cpu_temperature": "temperature"
    #   "cpu_load": "load"

    cpu_model = subprocess.run(["lscpu | grep 'Model name' | awk '{print $3}'"], capture_output=True,
                               text=True).stdout.strip()
    cpu_cores = subprocess.run(["lscpu | grep 'Core(s) per socket' | awk '{print $4}'"], capture_output=True,
                               text=True).stdout.strip()
    cpu_threads = subprocess.run(["lscpu | grep 'Thread(s) per core' | awk '{print $4}'"], capture_output=True,
                                 text=True).stdout.strip()
    cpu_frequency = subprocess.run(["lscpu | grep 'CPU MHz' | awk '{print $3}'"], capture_output=True,
                                   text=True).stdout.strip()
    cpu_usage = psutil.cpu_percent()
    cpu_temperature = subprocess.run(["sensors | grep 'Package id 0' | awk '{print $4}'"], capture_output=True,
                                     text=True).stdout.strip()
    cpu_load = psutil.getloadavg()

    return {
        "cpu_model": cpu_model,
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "cpu_frequency": cpu_frequency,
        "cpu_usage": cpu_usage,
        "cpu_temperature": cpu_temperature,
        "cpu_load": cpu_load
    }


def get_memory_info():
    #   "memory_total": "total",
    #   "memory_available": "available",
    #   "memory_used": "used",
    #   "memory_free": "free",
    #   "memory_shared": "shared",
    #   "memory_buffers": "buffers",
    #   "memory_cached": "cached",
    #   "memory_swap_total": "swap_total",
    #   "memory_swap_used": "swap_used",
    #   "memory_swap_free": "swap_free"

    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "memory_total": memory.total,
        "memory_available": memory.available,
        "memory_used": memory.used,
        "memory_free": memory.free,
        "memory_shared": memory.shared,
        "memory_buffers": memory.buffers,
        "memory_cached": memory.cached,
        "memory_swap_total": swap.total,
        "memory_swap_used": swap.used,
        "memory_swap_free": swap.free
    }


def get_kernel_info():
    #   "kernel_name": "name",
    #   "kernel_version": "version",
    #   "kernel_release": "release",
    #   "kernel_architecture": "architecture"

    kernel_name = subprocess.run(["uname -s"], capture_output=True, text=True).stdout.strip()
    kernel_version = subprocess.run(["uname -v"], capture_output=True, text=True).stdout.strip()
    kernel_release = subprocess.run(["uname -r"], capture_output=True, text=True).stdout.strip()
    kernel_architecture = subprocess.run(["uname -m"], capture_output=True, text=True).stdout.strip()

    return {
        "kernel_name": kernel_name,
        "kernel_version": kernel_version,
        "kernel_release": kernel_release,
        "kernel_architecture": kernel_architecture
    }


def get_linux_os_info():
    #   "linux_os_name": "name",
    #   "linux_os_version": "version",
    #   "linux_os_id": "id",
    #   "linux_os_id_like": "id_like",
    #   "linux_os_pretty_name": "pretty_name",
    #   "linux_os_version_codename": "version_codename",
    #   "linux_os_version_id": "version_id"

    linux_os_name = subprocess.run(["lsb_release -si"], capture_output=True, text=True).stdout.strip()
    linux_os_version = subprocess.run(["lsb_release -sr"], capture_output=True, text=True).stdout.strip()
    linux_os_id = subprocess.run(["lsb_release -si"], capture_output=True, text=True).stdout.strip()
    linux_os_id_like = subprocess.run(["lsb_release -si"], capture_output=True, text=True).stdout.strip()
    linux_os_pretty_name = subprocess.run(["lsb_release -si"], capture_output=True, text=True).stdout.strip()
    linux_os_version_codename = subprocess.run(["lsb_release -si"], capture_output=True, text=True).stdout.strip()
    linux_os_version_id = subprocess.run(["lsb_release -si"], capture_output=True, text=True).stdout.strip()

    return {
        "linux_os_name": linux_os_name,
        "linux_os_version": linux_os_version,
        "linux_os_id": linux_os_id,
        "linux_os_id_like": linux_os_id_like,
        "linux_os_pretty_name": linux_os_pretty_name,
        "linux_os_version_codename": linux_os_version_codename,
        "linux_os_version_id": linux_os_version_id
    }


def get_architecture_info():
    #   "architecture": "architecture"

    architecture = subprocess.run(["uname -m"], capture_output=True, text=True).stdout.strip()

    return {
        "architecture": architecture
    }


def get_uptime_info():
    #   "uptime": "uptime"

    uptime = subprocess.run(["uptime -p"], capture_output=True, text=True).stdout.strip()

    return {
        "uptime": uptime
    }


def get_interfaces_info():
    #   "interfaces": [
    #       {
    #           "name": "name",
    #           "mac_address": "mac_address",
    #           "ip_address": "ip_address",
    #           "netmask": "netmask",
    #           "broadcast": "broadcast",
    #           "mtu": "mtu",
    #           "status": "status"
    #       }
    #   ]

    ifaces = []

    for iface in psutil.net_if_addrs():
        if iface != "lo":
            iface_info = psutil.net_if_addrs()[iface]
            for ifc in iface_info:
                if ifc.family == 2:
                    ifaces.append({
                        "name": iface_info[0],
                        "mac_address": iface_info[0].address,
                        "ip_address": iface_info[1].address,
                        "netmask": iface_info[1].netmask,
                        "broadcast": iface_info[1].broadcast,
                        "mtu": iface_info[1],
                        "status": iface_info[1].ptp
                    })

    return {
        "interfaces": interfaces
    }


def get_routes_info():
    #   "routes": [
    #       {
    #           "destination": "destination",
    #           "gateway": "gateway",
    #           "netmask": "netmask",
    #           "flags": "flags",
    #           "metric": "metric",
    #           "ref": "ref",
    #           "use": "use",
    #           "interface": "interface"
    #       }
    #   ]

    routes = []

    for route in psutil.net_if_addrs():
        if route != "lo":
            route_info = psutil.net_if_addrs()[route]
            for rte in route_info:
                if rte.family == 2:
                    routes.append({
                        "destination": route_info[0],
                        "gateway": route_info[0].address,
                        "netmask": route_info[1].address,
                        "flags": route_info[1].netmask,
                        "metric": route_info[1].broadcast,
                        "ref": route_info[1],
                        "use": route_info[1].ptp,
                        "interface": route_info[1].ptp
                    })

    return {
        "routes": routes
    }


def get_arp_info():
    #   "arp": [
    #       {
    #           "ip_address": "ip_address",
    #           "mac_address": "mac_address",
    #           "interface": "interface",
    #           "age": "age"
    #       }
    #   ]

    arp = []

    for iface in psutil.net_if_addrs():
        if iface != "lo":
            iface_info = psutil.net_if_addrs()[iface]
            for ifce in iface_info:
                if ifce.family == 2:
                    arp.append({
                        "ip_address": iface_info[0],
                        "mac_address": iface_info[0].address,
                        "interface": iface_info[1].address,
                        "age": iface_info[1].netmask
                    })

    return {
        "arp": arp
    }


def get_netstat_info():
    #   "netstat": [
    #       {
    #           "protocol": "protocol",
    #           "local_address": "local_address",
    #           "foreign_address": "foreign_address",
    #           "state": "state",
    #           "pid": "pid"
    #       }
    #   ]

    netstat = []

    for connection in psutil.net_connections():
        if connection.status == "ESTABLISHED":
            netstat.append({
                "protocol": connection.family,
                "local_address": connection.laddr,
                "foreign_address": connection.raddr,
                "state": connection.status,
                "pid": connection.pid
            })

    return {
        "netstat": netstat
    }


def get_dhcpd_info():
    #   "dhcpd": [
    #       {
    #           "ip_address": "ip_address",
    #           "mac_address": "mac_address",
    #           "hostname": "hostname",
    #           "expires": "expires"
    #       }
    #   ]
    dhcpd_leases = []
    with open("/var/lib/dhcp/dhcpd.leases") as f:
        leases = f.read()
        leases = leases.split("lease")
        for lease in leases:
            if lease != "":
                dhcpd_leases.append({
                    "ip_address": lease.split(" ")[1].split("{")[0].strip(),
                    "mac_address": lease.split(" ")[2].split("{")[0].strip(),
                    "hostname": lease.split(" ")[3].split("{")[0].strip(),
                    "expires": lease.split(" ")[4].split("{")[0].strip()
                })
    dhcpd = []
    for lease in dhcpd_leases:
        dhcpd.append({
            "ip_address": lease["ip_address"],
            "mac_address": lease["mac_address"],
            "hostname": lease["hostname"],
            "expires": lease["expires"]
        })

    return {
        "dhcpd": dhcpd
    }


def get_system_time_info():
    #   "system_time": {
    #       "date": "date",
    #       "time": "time",
    #       "timezone": "timezone"
    #   }

    date = subprocess.run(["date +%d/%m/%Y"], capture_output=True, text=True).stdout.strip()
    time = subprocess.run(["date +%H:%M:%S"], capture_output=True, text=True).stdout.strip()
    timezone = subprocess.run(["date +%Z"], capture_output=True, text=True).stdout.strip()

    return {
        "system_time": {
            "date": date,
            "time": time,
            "timezone": timezone
        }
    }


def get_system_users_info():
    #   "system_users": [
    #       {
    #           "username": "username",
    #           "password": "password",
    #           "uid": "uid",
    #           "gid": "gid",
    #           "comment": "comment",
    #           "home": "home",
    #           "shell": "shell"
    #       }
    #   ]

    system_users = []
    for u in pwd.getpwall():
        system_users.append({
            "username": u.pw_name,
            "password": u.pw_passwd,
            "uid": u.pw_uid,
            "gid": u.pw_gid,
            "comment": u.pw_gecos,
            "home": u.pw_dir,
            "shell": u.pw_shell
        })

    return {
        "system_users": system_users
    }


def get_system_services_info():
    #   "system_services": [
    #       {
    #           "service_name": "service_name",
    #           "service_status": "service_status",
    #           "service_enabled": "service_enabled"
    #       }
    #   ]

    system_services = []

    for service in subprocess.run(["systemctl list-unit-files --type=service"], capture_output=True,
                                  text=True).stdout.strip().split("\n"):
        if service != "":
            service = service.split(" ")
            service = list(filter(None, service))
            system_services.append({
                "service_name": service[0],
                "service_status": subprocess.run(["systemctl is-active " + service[0]], capture_output=True,
                                                 text=True).stdout.strip(),
                "service_enabled": subprocess.run(["systemctl is-enabled " + service[0]], capture_output=True,
                                                  text=True).stdout.strip()
            })

    return {
        "system_services": system_services
    }


def get_system_packages_info():
    #   "system_packages": [
    #       {
    #           "package_name": "package_name",
    #           "package_version": "package_version",
    #           "package_description": "package_description"
    #       }
    #   ]

    system_packages = []

    for package in subprocess.run(["dpkg --get-selections"], capture_output=True, text=True).stdout.strip().split("\n"):
        if package != "":
            package = package.split("\t")
            package = list(filter(None, package))
            system_packages.append({
                "package_name": package[0],
                "package_version": subprocess.run(["dpkg -s " + package[0] + " | grep Version | awk '{print $2}'"],
                                                  capture_output=True, text=True).stdout.strip(),
                "package_description": subprocess.run(
                    ["dpkg -s " + package[0] + " | grep Description | awk '{print $2}'"], capture_output=True,
                    text=True).stdout.strip()
            })

    return {
        "system_packages": system_packages
    }


def get_system_firewall_info():
    #   "system_firewall": [
    #       {
    #           "rule_number": "rule_number",
    #           "rule": "rule"
    #       }
    #   ]

    system_firewall = []

    for rule in subprocess.run(["iptables -L -n"], capture_output=True, text=True).stdout.strip().split("\n"):
        if rule != "":
            rule = rule.split(" ")
            rule = list(filter(None, rule))
            system_firewall.append({
                "rule_number": rule[0],
                "rule": rule[1]
            })

    return {
        "system_firewall": system_firewall
    }


def get_system_fstab_info():
    #   "system_fstab": [
    #       {
    #           "device": "device",
    #           "mount_point": "mount_point",
    #           "file_system": "file_system",
    #           "options": "options",
    #           "dump": "dump",
    #           "pass": "pass"
    #       }
    #   ]

    system_fstab = []

    for line in subprocess.run(["cat /etc/fstab"], capture_output=True, text=True).stdout.strip().split("\n"):
        if line != "":
            line = line.split(" ")
            line = list(filter(None, line))
            system_fstab.append({
                "device": line[0],
                "mount_point": line[1],
                "file_system": line[2],
                "options": line[3],
                "dump": line[4],
                "pass": line[5]
            })

    return {
        "system_fstab": system_fstab
    }


def get_system_disks_info():
    #   "system_disks": [
    #       {
    #           "disk_name": "disk_name",
    #           "disk_size": "disk_size",
    #           "disk_used": "disk_used",
    #           "disk_available": "disk_available",
    #           "disk_use": "disk_use",
    #           "disk_mounted_on": "disk_mounted_on"
    #       }
    #   ]

    system_disks = []

    for line in subprocess.run(["df -h"], capture_output=True, text=True).stdout.strip().split("\n"):
        if line != "":
            line = line.split(" ")
            line = list(filter(None, line))
            system_disks.append({
                "disk_name": line[0],
                "disk_size": line[1],
                "disk_used": line[2],
                "disk_available": line[3],
                "disk_use": line[4],
                "disk_mounted_on": line[5]
            })

    return {
        "system_disks": system_disks
    }


def get_system_cellular_info():
    #   "system_cellular": {
    #       "cellular_status": "cellular_status",
    #       "cellular_signal": "cellular_signal",
    #       "cellular_operator": "cellular_operator"
    #   }

    cellular_status = subprocess.run(["cat /sys/class/net/ppp0/operstate"], capture_output=True,
                                     text=True).stdout.strip()
    if cellular_status == "up":
        cellular_signal = subprocess.run(["cat /sys/class/net/ppp0/statistics/signal_strength"], capture_output=True,
                                         text=True).stdout.strip()
        cellular_operator = subprocess.run(["cat /sys/class/net/ppp0/statistics/operator"], capture_output=True,
                                           text=True).stdout.strip()
    else:
        cellular_signal = None
        cellular_operator = None

    return {
        "system_cellular": {
            "cellular_status": cellular_status,
            "cellular_signal": cellular_signal,
            "cellular_operator": cellular_operator
        }
    }


def get_system_gps_info():
    #   "system_gps": {
    #       "gps_status": "gps_status",
    #       "gps_latitude": "gps_latitude",
    #       "gps_longitude": "gps_longitude",
    #       "gps_altitude": "gps_altitude",
    #       "gps_speed": "gps_speed",
    #       "gps_satellites": "gps_satellites"
    #   }

    gps_status = subprocess.run(["cat /sys/class/net/eth0/operstate"], capture_output=True, text=True).stdout.strip()
    if gps_status == "up":
        gps_latitude = subprocess.run(["cat /sys/class/net/eth0/statistics/latitude"], capture_output=True,
                                      text=True).stdout.strip()
        gps_longitude = subprocess.run(["cat /sys/class/net/eth0/statistics/longitude"], capture_output=True,
                                       text=True).stdout.strip()
        gps_altitude = subprocess.run(["cat /sys/class/net/eth0/statistics/altitude"], capture_output=True,
                                      text=True).stdout.strip()
        gps_speed = subprocess.run(["cat /sys/class/net/eth0/statistics/speed"], capture_output=True,
                                   text=True).stdout.strip()
        gps_satellites = subprocess.run(["cat /sys/class/net/eth0/statistics/satellites"], capture_output=True,
                                        text=True).stdout.strip()
    else:
        gps_latitude = None
        gps_longitude = None
        gps_altitude = None
        gps_speed = None
        gps_satellites = None

    return {
        "system_gps": {
            "gps_status": gps_status,
            "gps_latitude": gps_latitude,
            "gps_longitude": gps_longitude,
            "gps_altitude": gps_altitude,
            "gps_speed": gps_speed,
            "gps_satellites": gps_satellites
        }
    }


def get_system_vnstat_info():
    #   "system_vnstat": [
    #       {
    #           "vnstat_interface": "vnstat_interface",
    #           "vnstat_rx": "vnstat_rx",
    #           "vnstat_tx": "vnstat_tx"
    #       }
    #   ]

    system_vnstat = []

    for interface in psutil.net_if_addrs().keys():
        if interface != "lo":
            vnstat_rx = subprocess.run(["vnstat -i " + interface + " --oneline | awk '{print $3}'"],
                                       capture_output=True, text=True).stdout.strip()
            vnstat_tx = subprocess.run(["vnstat -i " + interface + " --oneline | awk '{print $4}'"],
                                       capture_output=True, text=True).stdout.strip()
            system_vnstat.append({
                "vnstat_interface": interface,
                "vnstat_rx": vnstat_rx,
                "vnstat_tx": vnstat_tx
            })

    return {
        "system_vnstat": system_vnstat
    }


def get_system_ipsec_vpn_info():
    #   "system_ipsec_vpn": {
    #       "ipsec_vpn_status": "ipsec_vpn_status",
    #       "ipsec_vpn_local_ip": "ipsec_vpn_local_ip",
    #       "ipsec_vpn_remote_ip": "ipsec_vpn_remote_ip",
    #       "ipsec_vpn_local_id": "ipsec_vpn_local_id",
    #       "ipsec_vpn_remote_id": "ipsec_vpn_remote_id",
    #       "ipsec_vpn_up_since": "ipsec_vpn_up_since"
    #   }

    ipsec_vpn_status = subprocess.run(["ipsec status | grep 'State:' | awk '{print $2}'"], capture_output=True,
                                      text=True).stdout.strip()
    if ipsec_vpn_status == "up":
        ipsec_vpn_local_ip = subprocess.run(["ipsec status | grep 'Local IP:' | awk '{print $3}'"], capture_output=True,
                                            text=True).stdout.strip()
        ipsec_vpn_remote_ip = subprocess.run(["ipsec status | grep 'Remote IP:' | awk '{print $3}'"],
                                             capture_output=True, text=True).stdout.strip()
        ipsec_vpn_local_id = subprocess.run(["ipsec status | grep 'Local ID:' | awk '{print $3}'"], capture_output=True,
                                            text=True).stdout.strip()
        ipsec_vpn_remote_id = subprocess.run(["ipsec status | grep 'Remote ID:' | awk '{print $3}'"],
                                             capture_output=True, text=True).stdout.strip()
        ipsec_vpn_up_since = subprocess.run(["ipsec status | grep 'Up since:' | awk '{print $3,$4,$5,$6}'"],
                                            capture_output=True, text=True).stdout.strip()
    else:
        ipsec_vpn_local_ip = None
        ipsec_vpn_remote_ip = None
        ipsec_vpn_local_id = None
        ipsec_vpn_remote_id = None
        ipsec_vpn_up_since = None

    return {
        "system_ipsec_vpn": {
            "ipsec_vpn_status": ipsec_vpn_status,
            "ipsec_vpn_local_ip": ipsec_vpn_local_ip,
            "ipsec_vpn_remote_ip": ipsec_vpn_remote_ip,
            "ipsec_vpn_local_id": ipsec_vpn_local_id,
            "ipsec_vpn_remote_id": ipsec_vpn_remote_id,
            "ipsec_vpn_up_since": ipsec_vpn_up_since
        }
    }


def get_system_openvpn_client_info():
    #   "system_openvpn_client": {
    #       "openvpn_client_status": "openvpn_client_status",
    #       "openvpn_client_local_ip": "openvpn_client_local_ip",
    #       "openvpn_client_remote_ip": "openvpn_client_remote_ip",
    #       "openvpn_client_up_since": "openvpn_client_up_since"
    #   }

    openvpn_client_status = subprocess.run(["systemctl is-active openvpn-client"], capture_output=True,
                                           text=True).stdout.strip()
    if openvpn_client_status == "active":
        openvpn_client_local_ip = subprocess.run(["ip a | grep tun0 | grep inet | awk '{print $2}' | cut -d '/' -f 1"],
                                                 capture_output=True, text=True).stdout.strip()
        openvpn_client_remote_ip = subprocess.run(["ip a | grep tun0 | grep inet | awk '{print $4}' | cut -d '/' -f 1"],
                                                  capture_output=True, text=True).stdout.strip()
        openvpn_client_up_since = subprocess.run([
            "systemctl show openvpn-client | grep 'ActiveEnterTimestamp=' | cut -d '=' -f 2 | cut -d '.' -f 1 | cut -d ' ' -f 2,3,4,5"],
            capture_output=True, text=True).stdout.strip()
    else:
        openvpn_client_local_ip = None
        openvpn_client_remote_ip = None
        openvpn_client_up_since = None

    return {
        "system_openvpn_client": {
            "openvpn_client_status": openvpn_client_status,
            "openvpn_client_local_ip": openvpn_client_local_ip,
            "openvpn_client_remote_ip": openvpn_client_remote_ip,
            "openvpn_client_up_since": openvpn_client_up_since
        }
    }


def get_system_openvpn_server_info():
    #   "system_openvpn_server": {
    #       "openvpn_server_status": "openvpn_server_status",
    #       "openvpn_server_local_ip": "openvpn_server_local_ip",
    #       "openvpn_server_remote_ip": "openvpn_server_remote_ip",
    #       "openvpn_server_up_since": "openvpn_server_up_since"
    #   }

    openvpn_server_status = subprocess.run(["systemctl is-active openvpn-server"], capture_output=True,
                                           text=True).stdout.strip()
    if openvpn_server_status == "active":
        openvpn_server_local_ip = subprocess.run(["ip a | grep tun0 | grep inet | awk '{print $2}' | cut -d '/' -f 1"],
                                                 capture_output=True, text=True).stdout.strip()
        openvpn_server_remote_ip = subprocess.run(["ip a | grep tun0 | grep inet | awk '{print $4}' | cut -d '/' -f 1"],
                                                  capture_output=True, text=True).stdout.strip()
        openvpn_server_up_since = subprocess.run([
            "systemctl show openvpn-server | grep 'ActiveEnterTimestamp=' | cut -d '=' -f 2 | cut -d '.' -f 1 | cut -d ' ' -f 2,3,4,5"],
            capture_output=True, text=True).stdout.strip()
    else:
        openvpn_server_local_ip = None
        openvpn_server_remote_ip = None
        openvpn_server_up_since = None

    return {
        "system_openvpn_server": {
            "openvpn_server_status": openvpn_server_status,
            "openvpn_server_local_ip": openvpn_server_local_ip,
            "openvpn_server_remote_ip": openvpn_server_remote_ip,
            "openvpn_server_up_since": openvpn_server_up_since
        }
    }


def get_system_journald_info():
    #   "system_journald": {
    #       "journald_logs": "journald_logs"
    #   }

    # Get 1000 lines of journald logs
    journald_logs = subprocess.run(["journalctl -n 1000"], capture_output=True, text=True).stdout.strip()

    return {
        "system_journald": {
            "journald_logs": journald_logs
        }
    }


def get_system_info():
    hostname = get_hostname()
    cpu = get_cpu_info()
    memory = get_memory_info()
    kernel = get_kernel_info()
    linos = get_linux_os_info()
    architecture = get_architecture_info()
    uptime = get_uptime_info()
    ifcs = get_interfaces_info()
    routes = get_routes_info()
    arp = get_arp_info()
    netstat = get_netstat_info()
    dhcpd = get_dhcpd_info()
    system_time = get_system_time_info()
    system_users = get_system_users_info()
    system_services = get_system_services_info()
    system_packages = get_system_packages_info()
    system_firewall = get_system_firewall_info()
    system_fstab = get_system_fstab_info()
    system_disks = get_system_disks_info()
    system_theme = get_system_theme_info()
    system_cellular = get_system_cellular_info()
    system_gps = get_system_gps_info()
    system_vnstat = get_system_vnstat_info()
    system_ipsec_vpn = get_system_ipsec_vpn_info()
    system_openvpn_client = get_system_openvpn_client_info()
    system_openvpn_server = get_system_openvpn_server_info()
    system_journald = get_system_journald_info()

    return {
        "hostname": hostname,
        "cpu": cpu,
        "memory": memory,
        "kernel": kernel,
        "linos": linos,
        "architecture": architecture,
        "uptime": uptime,
        "interfaces": ifcs,
        "routes": routes,
        "arp": arp,
        "netstat": netstat,
        "dhcpd": dhcpd,
        "system_time": system_time,
        "system_users": system_users,
        "system_services": system_services,
        "system_packages": system_packages,
        "system_firewall": system_firewall,
        "system_fstab": system_fstab,
        "system_disks": system_disks,
        "system_theme": system_theme,
        "system_cellular": system_cellular,
        "system_gps": system_gps,
        "system_vnstat": system_vnstat,
        "system_ipsec_vpn": system_ipsec_vpn,
        "system_openvpn_client": system_openvpn_client,
        "system_openvpn_server": system_openvpn_server,
        "system_journald": system_journald
    }


# Zip up the logs folder and system_info.json file and put in /workspace folder
def zip_logs():
    hostname = get_hostname()
    os.system("zip -r /home/{}/Desktop/workspace/{}system_config.zip /home/{}/Desktop/workspace{}config/*.*".format(user, hostname, user, hostname))


# Create Function to send the zip file to dropbox
def send_to_dropbox():
    hostname = get_hostname()
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
    )
    # Upload the zip file to dropbox
    with open("/home/{}/Desktop/workspace/system_config_{}.zip".format(user, hostname), "rb") as f:
        dbx.files_upload(f.read(), "/system_config_{}.zip".format(hostname), mute=True)


# Create main function
def create_logs_folder():
    hostname = get_hostname()
    # Create the logs folder
    os.system("mkdir /home/{}/Desktop/workspace/{}config/logs".format(user, hostname))


def create_scripts_folder():
    hostname = get_hostname()
    # Create the scripts folder
    os.system("mkdir /home/{}/Desktop/workspace/{}config/scripts".format(user, hostname))


def create_system_info_file():
    hostname = get_hostname()
    # Create the system_info.json file
    with open("/home/{}/Desktop/workspace/system_info.json".format(user), "w") as f:
        json.dump(get_system_info(), f, indent=4)

    # Move the system_info.json file to the {}config folder
    os.system("mv /home/{}/Desktop/workspace/system_info.json /home/{}/Desktop/workspace/{}config/system_info.json".format(user, user, hostname))
    # If system_info.json does not exist in /home/{}/ copy system_info.json to /home/{}/system_info.json
    # This will be the initial system_info.json file that config_parse_apply.py will use to compare against
    if not os.path.exists("/home/{}/system_info.json".format(user)):
        os.system("cp /home/{}/Desktop/workspace/{}config/system_info.json /home/{}/system_info.json".format(user, hostname, user))


def main():
    # Create the logs folder
    create_logs_folder()
    # Create the system_info.json file
    create_system_info_file()
    # Zip up the logs folder and system_info.json file
    zip_logs()
    # Send the zip file to dropbox
    send_to_dropbox()


# Run the main function
if __name__ == "__main__":
    main()
