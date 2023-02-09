#!/bin/python3
import dropbox
import json


# This script is for parsing the system_config zip file and applying any changes to the system
from config_grabber import *

# This function is for applying the changes to the system


# Get zip file from Dropbox
def get_zip():
    # Get zip file from Dropbox
    hostname = get_hostname()
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
    )
    # Upload the zip file to dropbox
    with open("/home/{}/Desktop/workspace/system_config_{}.zip".format(user, hostname), "rb") as f:
        dbx.files_download("/system_config_{}.zip".format(hostname))
        print("Downloaded zip file from Dropbox")


# Unzip the file
def unzip():
    # Unzip the file
    hostname = get_hostname()
    os.system("unzip /home/{}/Desktop/workspace/system_config_{}.zip".format(user, hostname))
    print("Unzipped file")


# Apply the changes
def apply_changes():
    # Look in system_config{} folder for system_info.json
    hostname = get_hostname()
    with open("/home/{}/Desktop/workspace/system_config_{}/system_info.json".format(user, hostname), "r") as f:
        system_info = json.load(f)
        print("Loaded system_info.json")
    # Compare /home/{}/system_info.json to /home/{}/Desktop/workspace/system_config_{}/system_info.json
    with open("/home/{}/system_info.json".format(user), "r") as current_f:
        system_info = json.load(f)
        print("Loaded current system_info.json")

    with open("/home/{}/Desktop/workspace/system_config_{}/system_info.json".format(user, hostname), "r") as new_f:
        new_system_info = json.load(f)
        print("Loaded new system_info.json")
    if system_info == new_system_info:
        print("No changes to apply")
    else:
        make_system_changes()


# Make the changes to the system
def change_hostname():
    hostname = get_hostname()
    os.system("hostnamectl set-hostname {}".format(hostname))


def change_interfaces_info():
    pass


def change_routes_info():
    pass


def change_dhcpd_info():
    pass


def change_arp_info():
    pass


def change_system_users_info():
    pass


def change_system_services_info():
    pass


def change_system_packages_info():
    pass


def change_system_firewall_info():
    pass


def change_system_fstab_info():
    pass


def change_system_disks_info():
    pass


def change_system_theme_info():
    hostname = get_hostname()
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
    with open("/home/{}/Desktop/workspace/system_config_{}/system_info.json".format(user, hostname), "r") as f:
        system_info = json.load(f)
        print("Loaded system_info.json")
        if f
    application_style = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_application_style"]))
    plasma_style = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_plasma_style"]))
    color_scheme = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_color_scheme"]))
    window_decoration = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_window_decoration"]))
    font = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_font"]))
    icons = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_icons"]))
    cursor = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_cursor"]))
    wallpaper = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_wallpaper"]))
    splash_screen = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_splash_screen"]))
    login_screen = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_login_screen"]))
    lock_screen = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_lock_screen"]))
    global_theme = os.system("kwriteconfig5 --file kdeglobals --group General --key widgetStyle {}".format(
        system_info["theme_global_theme"]))




def change_system_ipsec_vpn_info():
    pass


def change_system_openvpn_client_info():
    pass


def change_system_openvpn_server_info():
    pass


def make_system_changes():
    hostname = change_hostname()
    ifcs = change_interfaces_info()
    routes = change_routes_info()
    arp = change_arp_info()
    dhcpd = change_dhcpd_info()
    system_users = change_system_users_info()
    system_services = change_system_services_info()
    system_packages = change_system_packages_info()
    system_firewall = change_system_firewall_info()
    system_fstab = change_system_fstab_info()
    system_disks = change_system_disks_info()
    system_theme = change_system_theme_info()
    system_ipsec_vpn = change_system_ipsec_vpn_info()
    system_openvpn_client = change_system_openvpn_client_info()
    system_openvpn_server = change_system_openvpn_server_info()