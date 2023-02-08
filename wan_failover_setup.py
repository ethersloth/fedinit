#!/bin/python3

# Import modules
import os

from firewall_setup import external_zone_interfaces

# variables
failover_priority = []


# Using the external_zone_interfaces list, ask user to select each interface in order of failover priority, append to failover_priority list
def set_failover_priority():
    if len(external_zone_interfaces) < 1:
        pass
    else:
        print(external_zone_interfaces)
        failover = input(
            'Enter the interface {} in order of failover priority: (First entry will have highest priority, Last entry will have lowest. ')
        if failover in external_zone_interfaces:
            failover_priority.append(failover)
            external_zone_interfaces.remove(failover)
            if len(external_zone_interfaces) > 0:
                set_failover_priority()
            else:
                print("Failover priority set")
        else:
            print("Invalid interface")
            set_failover_priority()
        print(failover_priority)
    ask_confirm_priority = input('Are you satisfied with the failover priority? (Y/N): If not we will start over. ')
    if ask_confirm_priority == 'Y' or ask_confirm_priority == 'y':
        set_wan_failover_service()
    else:
        failover_priority.clear()
        set_failover_priority()


# Set the wan failover.py script as a service that runs on boot
def set_wan_failover_service():
    from fedinitinstall import user
    os.system("cp /home/{}/wan_failover.py /etc/wan_failover.py".format(user))
    os.system("chmod +x /etc/wan_failover.py")
    os.system("chown root:root /etc/wan_failover.py")
    os.system("chmod 755 /etc/wan_failover.py")
    create_wan_failover_service()


# Create a service file for the wan failover.py script
def create_wan_failover_service():
    os.system("touch /etc/systemd/system/wan_failover.service")
    os.system("echo '[Unit]' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'Description=wan_failover' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'After=network.target' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '[Service]' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'Type=simple' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'ExecStart=/usr/bin/python3 /etc/wan_failover.py' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '' >> /etc/systemd/system/wan_failover.service")
    os.system("echo '[Install]' >> /etc/systemd/system/wan_failover.service")
    os.system("echo 'WantedBy=multi-user.target' >> /etc/systemd/system/wan_failover.service")
    os.system("systemctl daemon-reload")
    os.system("systemctl enable wan_failover.service")
    os.system("systemctl start wan_failover.service")


# Main Function
def main():
    set_failover_priority()


if __name__ == '__main__':
    main()
