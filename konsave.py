#!/bin/python3

# Import modules
import os

# Variables


# Download files
def download_files():
    os.system("wget -N https://www.dropbox.com/s/wqii3x5dz1q4btk/gwhitlock.knsv?dl=1 -O gwhitlock.knsv")


# Apply Konsave Theme
def apply_theme():
    os.system("konsave -i gwhitlock.knsv")
    os.system("konsave -a gwhitlock")


# Main Function
def main():
    download_files()
    apply_theme()


if __name__ == '__main__':
    main()