#!/bin/python3
import os
import dropbox


def download_ssh_key():
    dbx = dropbox.Dropbox(
            app_key='9qx5m6wmf51e811',
            app_secret='r4dcl1g70xg9a4i',
            oauth2_refresh_token='0sQRFeebAW8AAAAAAAAAAcCneydNSUS4O4mednoRiB-uqQk05FJBG-zDXfAsXBB-'
        )
    metadata, res = dbx.files_download(path='/ssh_keys.txt')
    with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'wb') as f:
        f.write(res.content)


# Apply HAL9001 Public Key to authorized_keys
def apply_ssh_key():
    os.system("cat /home/gwhitlock/Desktop/workspace/ssh_keys.txt >> /home/gwhitlock/.ssh/authorized_keys")
    os.system("cat /home/gwhitlock/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys")
    os.system("rm -rf /home/gwhitlock/Desktop/workspace/ssh_keys.txt")


# Set SSH to only allow key based authentication
def set_ssh_config():
    os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    os.system("systemctl restart sshd")


def run_other_scripts():
    os.system('/bin/python3 config_grabber.py')
    os.system('/bin/python3 network.py')
    os.system('/bin/python3 ipsec.py')
    os.system('/bin/python3 openvpnser.py')
    os.system('/bin/python3 nextcloud.py')
    os.system('/bin/python3 jellyfin.py')
    os.system('/bin/python3 airsonic.py')


# Main function
def main():
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()
    run_other_scripts()
