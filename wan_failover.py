#!/bin/python3

# This script is to be run from a systemd timer to check the status of the WAN connection
# Using the failover_priority list, the script will setup all interfaces as wan in order of priority
# If the interface is not connected, the script will move on to the next interface in the list, while keeping the previous interface up to continue the ping test
# If the interface is connected, the script will set the interface as the default route and continue the ping test on the old interface
# If the ping test starts to succeed for the old interface, the script will set the old interface as the default route and set the new interface as backup
# Here is the order of operations:
# 1. set the first interface in the list as wan/default route then run a ping test on this interface (8.8.8.8)
# 2. if the ping test fails, set the next interface in the list as wan/default route then run a second ping test on this interface (8.8.8.8)
# 3. If the ping test on the first interface shows connection again, set the first interface as the default route and set the second interface as backup
# 4. If instead the ping test on the second interface fails, while the ping test on the first interface is still failing, setup the third interface as wan/default route and run a third ping test on this interface (8.8.8.8)
# 5. Do this recursively for all interfaces in the list even if the ping test for each interface fails
# 6. If the ping test for all interfaces in the list fails, keeps all tests running until one of the interfaces shows connection again, then set that interface as the default route
# 7. Finally, make sure that the default route is set to the interface with the highest priority in the list
import subprocess
import os
import time
from fedinitinstall import failover_priority

failed_interfaces = []
wan_interface = []
failed_int_that_worked = []


def ping_test(interface):
    count = 0
    os.system("nmcli connection modify {} ipv4.route-metric 100".format(interface))
    for ping in range(5):
        result = subprocess.run(['ping', '-I', {}, '-c', '1', '8.8.8.8'.format(interface)], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            count += 1
    if count >= 3:
        log_ping_test(interface, "Connected")
        return True
    else:
        log_ping_test(interface, "Disconnected/Failed")
        return False


# Set the first interface in the list as wan/default route
def set_wan_interface(interface):
    os.system("nmcli connection modify {} ipv4.route-metric 0".format(interface))
    os.system("nmcli connection up {} ifname {}".format(interface, interface))


# Go through the list of interfaces in the failover_priority, run a ping test on that interface, and if successful, set that interface as the default route, otherwise add that interface to the failed_interfaces list and move on to the next interface in the list
def check_wan_connection():
    for interface in failover_priority:
        global wan_interface
        ping_test(interface)
        if ping_test(interface) is True:
            set_wan_interface(interface)
            wan_interface.append(interface)
            break

        else:
            failed_interfaces.append(interface)
            continue


# Once the wan_interface is set, run a ping test on the wan_interface every 5 minutes
def ping_test_wan_interface():
    while True:
        ping_test(wan_interface[0])
        time.sleep(300)
        if ping_test(wan_interface[0]) is False:
            check_wan_connection()
            break
        else:
            continue


# Run a ping on all interfaces in the failed_interfaces list every 5 minutes
def ping_test_failed_interfaces():
    while True:
        for interface in failed_interfaces:
            ping_test(interface)
            time.sleep(300)
            if ping_test(interface) is True:
                failed_int_that_worked.append(interface)
                break
            else:
                continue
        if len(failed_interfaces) < 1:
            break
        else:
            continue


# Compare the failed_int_that_worked list to the failover_priority list and if an interface in the failed_int_that_worked list has a higher priority than the wan_interface, set that interface as the default route
def compare_failed_int_to_wan_int():
    for interface in failed_int_that_worked:
        if failover_priority.index(interface) < failover_priority.index(wan_interface[0]):
            set_wan_interface(interface)
            break
        else:
            continue


# Log the ping test results with timestamp and interface name
def log_ping_test(interface, result):
    with open('/var/log/ping_test.log', 'a') as f:
        f.write(time.ctime() + " " + interface + " " + result)


# Main function
def main():
    check_wan_connection()
    ping_test_wan_interface()
    ping_test_failed_interfaces()
    compare_failed_int_to_wan_int()


if __name__ == "__main__":
    main()
