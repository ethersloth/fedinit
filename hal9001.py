#!/bin/python3
import os
import dropbox


# Download files
def download_files():
    os.system("wget -N https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1 -O gwhitlock.knsv")


# Apply Konsave Theme
def apply_theme():
    os.system("konsave -i gwhitlock.knsv")
    os.system("konsave -a gwhitlock")


# Install Barrier
def install_barrier():
    os.system("dnf -y install barrier")


# Get The SSH Public Key
def get_ssh_key():
    # Create public key file
    os.system("ssh-keygen -t ed25519 -C 'ramboy17@hotmail.com' -f /root/.ssh/id_rsa -N ''")
    os.system("ssh-keygen -t ed25519 -C 'ramboy17@hotmail.com' -f /home/gwhitlock/.ssh/id_rsa -N ''")
    os.system("cat /root/.ssh/id_rsa.pub >> /home/gwhitlock/Desktop/workspace/ssh_keys.txt")
    # Append gwhitlock public key to ssh_keys.txt
    os.system("cat /home/gwhitlock/.ssh/id_rsa.pub >> /home/gwhitlock/Desktop/workspace/ssh_keys.txt")


# Upload SSH Public Key To Dropbox
def upload_ssh_key():
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
    )
    with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'rb') as f:
        dbx.files_upload(f.read(), '/ssh_keys.txt', mode=dropbox.files.WriteMode.overwrite)


# Set SSH to only allow key based authentication
def set_ssh_config():
    os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    os.system("systemctl restart sshd")


# Main Function
def main():
    get_ssh_key()
    upload_ssh_key()
    set_ssh_config()
    # install_barrier()
    # download_files()
    # apply_theme()


if __name__ == '__main__':
    main()
