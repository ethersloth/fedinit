#!/bin/python3
import os

os.system('/bin/python3 config_grabber.py')
os.system('/bin/python3 network.py')
os.system('/bin/python3 ipsec.py')
os.system('/bin/python3 openvpnser.py')
os.system('/bin/python3 openvpnclient.py')
os.system('/bin/python3 nextcloud.py')
os.system('/bin/python3 jellyfin.py')
os.system('/bin/python3 airsonic.py')

