#!/bin/python3

import json
import os
import platform
import subprocess
import dropbox
import zipfile


def cpu_temp():
    # Get CPU temperature for Every Core, use sensors command
    cpu_temp_process = subprocess.run(["sensors"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return cpu_temp_process


def cell_modem_stats():
    # For every cell modem, get the following stats:
    # - CSQ Ex: -113 dBm
    # - ECIO Ex: -10 dBm
    # - Service Technology Ex: LTE
    # - RSRP Ex: -113 dBm
    # - RSRQ Ex: -10 dBm
    # - TMP Ex: 40 C
    # All Modems are in /dev/cdc-wdm*
    # Use qmicli and/or mmcli to get the stats
    cell_modem_stats = {}
    cell_modems = subprocess.run(["ls", "/dev/cdc-wdm*"], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")
    for cell_modem in cell_modems:
        if cell_modem != "":
            cell_modem_stats[cell_modem] = {}
            cell_modem_stats[cell_modem]["CSQ"] = subprocess.run(["qmicli", "-d", cell_modem, "qmi_nas_get_signal_request_rssi"], stdout=subprocess.PIPE).stdout.decode("utf-8")
            cell_modem_stats[cell_modem]["ECIO"] = subprocess.run(["qmicli", "-d", cell_modem, "qmi_nas_get_signal_request_ecio"], stdout=subprocess.PIPE).stdout.decode("utf-8")
            cell_modem_stats[cell_modem]["Service Technology"] = subprocess.run(["qmicli", "-d", cell_modem, "qmi_nas_get_signal_request_service_technology"], stdout=subprocess.PIPE).stdout.decode("utf-8")



def auth_log():
    # Use journalctl to grep for auth.service
    get_auth_log = subprocess.run(["journalctl", "-u", "auth.service"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return get_auth_log


def ssh_log():
    # Use journalctl to grep for sshd.service
    get_ssh_log = subprocess.run(["journalctl", "-u", "sshd.service"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return get_ssh_log


def gather_directory_tree(path):
    # Gather the directory tree of a given path, skip /proc and /sys
    directory_tree = {}
    # make sure ls -al output is not shown in console
    path = subprocess.run(["ls", "-al", path], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")
    for item in path:
        # make sure to skip /proc and /sys and any other directories that are not files or directories also don't show ls -al output in console
        if item != "" and item.split(" ")[-1] != "proc" and item.split(" ")[-1] != "sys":
            if item.split(" ")[0][0] == "d":
                directory_tree[item.split(" ")[-1]] = gather_directory_tree(f"{path}/{item.split(' ')[-1]}")
            else:
                directory_tree[item.split(" ")[-1]] = item.split(" ")[0]
    return directory_tree


def gather_vpn_configs():
    vpn_configs = {}
    for vpn in ["ipsec", "openvpn", "gre", "wireguard", "zerotier"]:
        try:
            vpn_config = subprocess.run(["cat", f"/etc/{vpn}/config"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if vpn_config.returncode == 0:
                vpn_configs[vpn] = vpn_config.stdout.decode("utf-8")
        except Exception as e:
            print(e)
            pass
    return vpn_configs


def gather_network_interface_info():
    network_interface_info = {}
    interfaces = subprocess.run(["ip", "a"], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")
    for interface in interfaces:
        if "state" in interface:
            interface_name = interface.split(":")[1].strip()
            interface_state = interface.split("state")[1].split(" ")[1].strip()
            network_interface_info[interface_name] = interface_state
    return network_interface_info


def gather_firewall_rules():
    # Figure out if OS is running iptables, nftables, or firewalld, or ufw
    try:
        subprocess.run(["which", "iptables"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).check_returncode()
        firewall = "iptables"
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["which", "nft"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).check_returncode()
            firewall = "nftables"
        except subprocess.CalledProcessError:
            try:
                subprocess.run(["which", "firewalld"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).check_returncode()
                firewall = "firewalld"
            except subprocess.CalledProcessError:
                try:
                    subprocess.run(["which", "ufw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).check_returncode()
                    firewall = "ufw"
                except subprocess.CalledProcessError:
                    firewall = "unknown"
    # Gather firewall rules
    if firewall == "iptables":
        firewall_rules = subprocess.run(["iptables", "-L"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    elif firewall == "nftables":
        firewall_rules = subprocess.run(["nft", "list", "ruleset"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    elif firewall == "firewalld":
        firewall_rules = subprocess.run(["firewall-cmd", "--list-all"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    elif firewall == "ufw":
        firewall_rules = subprocess.run(["ufw", "status"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    else:
        firewall_rules = "unknown"
    return firewall_rules


def gather_users_groups():
    users_info = {}
    users = subprocess.run(["cat", "/etc/passwd"], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")
    for user in users:
        if user:
            username = user.split(":")[0]
            user_id = user.split(":")[2]
            user_group_id = user.split(":")[3]
            user_home = user.split(":")[5]
            users_info[username] = {"user_id": user_id, "user_group_id": user_group_id, "user_home": user_home}
    return users_info


def gather_system_info():
    system_info = {"hostname": platform.node(), "os": platform.system(), "os_release": platform.release(),
                   "linux_distro": subprocess.run(["cat", "/etc/os-release"], stdout=subprocess.PIPE).stdout.decode("utf-8"),
                   "os_version": platform.version(), "architecture": platform.machine(), "cpu": platform.processor(),
                   "cpu_count": os.cpu_count(), "cpu_temp": cpu_temp(), "cell_modem_stats": cell_modem_stats(),
                   "auth_log": auth_log(), "ssh_log": ssh_log(), "vpn_configs": gather_vpn_configs(), "network_interface_info": gather_network_interface_info(),
                   "firewall_rules": gather_firewall_rules(), "users_groups": gather_users_groups(), "directory_tree": gather_directory_tree("/")}
    return system_info


# Create a folder to include scripts and config files
def create_folder():
    try:
        os.mkdir("Scripts")
    # If folder already exists, pass
    except FileExistsError:
        # Check to see if the folder contains bash or python scripts
        if os.path.exists("Scripts"):
            script_execution()


# If Credentials folder exists, and script files found, run scripts
def script_execution():
    # Check to see if the folder contains bash or python scripts
    if os.path.exists("Scripts"):
        # If folder exists, check to see if it contains bash or python scripts
        for file in subprocess.run(["ls", "Scripts"], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n"):
            if file.endswith(".sh"):
                try:
                    subprocess.run(["bash", f"Scripts/{file}"])
                    script_cleanup()
                except subprocess.CalledProcessError:
                    script_cleanup()
            elif file.endswith(".py"):
                try:
                    subprocess.run(["python3", f"Scripts/{file}"])
                    script_cleanup()
                except subprocess.CalledProcessError:
                    script_cleanup()


# Remove scripts folder after execution
def script_cleanup():
    try:
        subprocess.run(["rm", "-rf", "Scripts"])
    except subprocess.CalledProcessError:
        pass


# Create json file with system info
def create_json_file():
    try:
        with open("system_info.json", "w") as f:
            json.dump(gather_system_info(), f, indent=4)
    except Exception as e:
        print(e)
        pass


# Create a zip file with system info and Scripts folder at the root
def create_zip_file():
    try:
        with zipfile.ZipFile("system_info.zip", "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write("system_info.json")
            if os.path.exists("Scripts"):
                for file in subprocess.run(["ls", "Scripts"], stdout=subprocess.PIPE).stdout.decode("utf-8").split(
                        "\n"):
                    zip_file.write(f"Scripts/{file}")
    except Exception as e:
        print(e)
        pass


# Upload zip file to dropbox
def upload_to_dropbox():
    try:
        with open("system_info.zip", "rb") as f:
            data = f.read()
            dbx = dropbox.Dropbox(
                app_key='9qx5m6wmf51e811',
                app_secret='r4dcl1g70xg9a4i',
                oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP')
            dbx.files_upload(data, '/system_info.zip', mode=dropbox.files.WriteMode.overwrite)
    except Exception as e:
        print(e)
        pass


def main():
    create_folder()
    create_json_file()
    create_zip_file()
    upload_to_dropbox()


if __name__ == "__main__":
    main()
