#!/bin/python3
import json_delta

# This script is for parsing the system_config zip file and applying any changes to the system
from config_grabber import *

# from fedinitinstall import user
user = os.environ['user']

# This function is for applying the changes to the system


# Get zip file from Dropbox
def get_zip():
    # Get zip file from Dropbox
    user = 'gwhitlock'
    hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()
    dbx = dropbox.Dropbox(
        app_key='9qx5m6wmf51e811',
        app_secret='r4dcl1g70xg9a4i',
        oauth2_refresh_token='9Qbt7Z6yN-8AAAAAAAAAAY5r4cdPfoIOEN0wCU1IhiNt8ThM-tYgoAjpxuYDxscP'
    )
    # Upload the zip file to dropbox
    with open("/home/{}/Desktop/workspace/./config/system_config_{}.zip".format(user, hostname), "rb") as f:
        dbx.files_upload(f.read(), "/system_config_{}.zip".format(hostname), mode=dropbox.files.WriteMode.overwrite)
    print("Uploaded zip file to Dropbox")


# Unzip the file
def unzip():
    # Unzip the file
    user = 'gwhitlock'
    hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()
    os.system("unzip /home/{}/Desktop/workspace/system_config_{}.zip".format(user, hostname))
    print("Unzipped file")


def compare_files():
    # Compare the files
    user = 'gwhitlock'
    hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()
    with open("/home/{}/system_config.json".format(user), "r") as f:
        old_config = json.load(f)
    with open("/home/{}/Desktop/workspace/system_config_{}.json".format(user, hostname), "r") as f:
        new_config = json.load(f)
    changes = json_delta.diff(old_config, new_config)
    print(changes)

    delta = json_delta.diff(old_config, new_config)
    print(delta)
    if delta:
        print("Changes detected")
        apply_changes()


def apply_changes():
