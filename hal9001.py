#!/bin/python3
import os
import dropbox


# Download files
def download_files():
    os.system("wget -N https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1 -O gwhitlock.knsv")


# Apply Konsave Theme
def apply_theme():
    os.system("konsave -i gwhitlock.knsv")


# Install Barrier
def install_barrier():
    os.system("dnf -y install barrier")


# Get The SSH Public Key
def get_ssh_key():
    os.system("cat /root/.ssh/id_rsa.pub >> /home/gwhitlock/Desktop/workspace/ssh_keys.txt")
    # Append gwhitlock public key to ssh_keys.txt
    os.system("cat /home/gwhitlock/.ssh/id_rsa.pub >> /home/gwhitlock/Desktop/workspace/ssh_keys.txt")


# Upload SSH Public Key To Dropbox
def upload_ssh_key():
    dbx = dropbox.Dropbox(
        'sl.BX3VVSTTHKAg2tQvY5LLIEbgtwW29pRUaQl6KbgklwKQI98ZWt2UPXXFLhstXSPYDZJQcB0L9jHlS-FwAZk7ybl0JPeUT1w8zcKqzZAwBcf0TRtPBZcARLaVzRtwJ4HJNiMeb9g')
    with open('/home/gwhitlock/Desktop/workspace/ssh_keys.txt', 'rb') as f:
        dbx.files_upload(f.read(), '/ssh_keys.txt', mode=dropbox.files.WriteMode.overwrite)


# Set SSH to only allow key based authentication
def set_ssh_config():
    os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    os.system("systemctl restart sshd")
