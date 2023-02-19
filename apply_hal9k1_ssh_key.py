#!/bin/python3

# Import modules
import os
import dropbox
from fedinitinstall import user


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
    # Create .ssh directory if it doesn't exist
    os.system("mkdir -p /home/{}/.ssh".format(user))
    os.system("mkdir -p /root/.ssh")
    # Create authorized_keys file if it doesn't exist
    os.system("touch /home/{}/.ssh/authorized_keys".format(user))
    os.system("touch /root/.ssh/authorized_keys")
    # Append HAL9001 Public Key to authorized_keys
    os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /home/{}/.ssh/authorized_keys".format(user, user))
    os.system("cat /home/{}/Desktop/workspace/ssh_keys.txt >> /root/.ssh/authorized_keys".format(user))
    os.system("rm -rf /home/{}/Desktop/workspace/ssh_keys.txt".format(user))
    # Set permissions on authorized_keys
    os.system("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
    os.system("chmod 600 /root/.ssh/authorized_keys")


# Set SSH to only allow key based authentication
def set_ssh_config():
    os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    os.system("systemctl restart sshd")


# Main function
def main():
    download_ssh_key()
    apply_ssh_key()
    set_ssh_config()


if __name__ == '__main__':
    main()
