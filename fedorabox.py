#!/bin/python3

import os
import dropbox


# Download SSH Public Key From Dropbox
def download_ssh_key():
    dbx = dropbox.Dropbox(
        'sl.BX3VVSTTHKAg2tQvY5LLIEbgtwW29pRUaQl6KbgklwKQI98ZWt2UPXXFLhstXSPYDZJQcB0L9jHlS-FwAZk7ybl0JPeUT1w8zcKqzZAwBcf0TRtPBZcARLaVzRtwJ4HJNiMeb9g')
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