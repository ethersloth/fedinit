#!/bin/python3

# Import modules
import os
from fedinitinstall import user


# Variables


# Download files
def download_files():
    # Download Konsave knsv file
    os.system(
        "wget  https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1" + " -O /home/{}/Desktop/workspace/{}.knsv".format(
            user, user))


# Apply Konsave Theme
def apply_theme():
    os.system("sudo -u {} konsave -w".format(user))
    os.system("sudo -u {} konsave -i /home/{}/Desktop/workspace/{}.knsv".format(user, user, user))
    os.system("sudo -u {} konsave -a /home/{}/Desktop/workspace/{}".format(user, user, user))


# Main Function
def main():
    download_files()
    apply_theme()


if __name__ == '__main__':
    main()
