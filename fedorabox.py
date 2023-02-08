#!/bin/python3

import os
import dropbox


# Download SSH Public Key From Dropbox
def download_ssh_key():
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
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
