#!/bin/python3
import os
import dropbox
from fedinitinstall import user


# Run konsave.py
def apply_theme():
    os.system("python3 /home/{}/Dekstop/workspace/Scripts/konsave.py".format(user))


# Install Barrier
def install_barrier():
    os.system("dnf -y install barrier")


# Create SSH Private/Public Key Pair
def create_ssh_key():
    os.system("ssh-keygen -t rsa -b 4096 -C 'ramboy17@hotmail.com' -f /home/{}/.ssh/id_rsa -N ''".format(user))
    os.system("systemctl restart sshd")


# Create ssh_keys.txt file from /root/.ssh/id_rsa.pub and /home/{}/.ssh/id_rsa.pub.format(user)
def create_ssh_keys_txt():
    os.system("touch /home/{}/Dekstop/workspace/ssh_keys.txt".format(user))
    os.system("cat /root/.ssh/id_rsa.pub >> /home/{}/Dekstop/workspace/ssh_keys.txt".format(user))
    os.system("cat /home/{}/.ssh/id_rsa.pub >> /home/{}/Dekstop/workspace/ssh_keys.txt".format(user, user))
    os.system("chmod 600 /home/{}/Dekstop/workspace/ssh_keys.txt".format(user))


# Upload ssh_keys.txt to Dropbox
def upload_ssh_keys_txt():
    with open('/home/{}/Dekstop/workspace/ssh_keys.txt'.format(user), 'rb') as f:
        data = f.read()
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP')
    dbx.files_upload(data, '/ssh_keys.txt', mode=dropbox.files.WriteMode.overwrite)


# External Drive
def mount_external_drive():
    os.system("/bin/python3 /home/{}/Dekstop/workspace/Scripts/external_drive.py".format(user))


# Setup Firewall
def setup_firewall():
    os.system("/bin/python3 /home/{}/Dekstop/workspace/Scripts/firewall_setup.py".format(user))


def setup_wan_failover():
    from fedinitinstall import user
    input("Would you like to setup WAN Failover? (Y/N)")
    if input == 'Y' or input == 'y':
        os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/wan_failover_setup.py".format(user))
    elif input == 'N' or input == 'n':
        print("Not setting up WAN Failover.")
        exit(1)
    else:
        print("Invalid input. Not setting up WAN Failover.")
        setup_wan_failover()


# Ask user if they want to setup a VPN (IPSec or OpenVPN)
def setup_vpn():
    from fedinitinstall import user
    input("Would you like to setup a VPN? (Y/N)")
    if input == 'Y' or input == 'y':
        # Ask user if they want to setup an IPSec VPN or OpenVPN
        input("Would you like to setup an IPSec VPN or OpenVPN? (I/O)")
        if input == 'I' or input == 'i':
            os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/ipsec_vpn.py".format(user))
        elif input == 'O' or input == 'o':
            os.system("/bin/python3 /home/{}/Desktop/workspace/Scripts/openvpnclient.py".format(user))
        else:
            print("Invalid input. Not setting up VPN.")
            setup_vpn()
    elif input == 'N' or input == 'n':
        print("Not setting up VPN.")
        exit(1)
    else:
        print("Invalid input. Not setting up VPN.")
        setup_vpn()


# Main Function
def main():
    apply_theme()
    install_barrier()
    mount_external_drive()
    setup_firewall()
    setup_vpn()
    setup_wan_failover()


if __name__ == '__main__':
    main()
