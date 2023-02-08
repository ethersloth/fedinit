#!/bin/python3
import ipaddress
import os


def get_client_subnet():
    # Get the client subnet
    client_subnet = input('Enter the client subnet (ex.192.168.1.0 255.255.255.0): ')
    # Validate the client subnet
    while not ipaddress.ip_network(client_subnet, strict=False):
        client_subnet = input('Invalid subnet. Enter a valid subnet (ex.192.168.1.0 255.255.255.0): ')
    # Write Client subnet to file as Client Subnet x.x.x.x x.x.x.x
    with open('ip_subnet.txt', 'a') as f:
        f.write(get_client_name() + ":" + client_subnet)
        f.close()
    return client_subnet


def get_client_name():
    # Get the client name
    client_name = input('Enter the client name: ')
    with open('client_names.txt', 'r') as f:
        client_names = f.read()
        if client_name in client_names:
            print('Client name already exists. Please enter a different name.')
            client_name = input('Enter the client name: ')
    # Validate the client name
    while not client_name.isalnum():
        client_name = input('Invalid client name. Enter a valid client name: ')
        # append client_name to client_names list
        with open('client_names.txt', 'a') as f:
            f.write(client_name + '\n')
    return client_name


# Get Port from openvpnser.py
def get_port():
    from openvpnser import get_port
    port = get_port()
    return port


# Get Proto from openvpnser.py
def get_proto():
    from openvpnser import get_proto
    proto = get_proto()
    return proto


# Get remote ip automatically if not ask user to enter it
def get_remote_ip():
    import requests
    try:
        response = requests.get('http://checkip.dyndns.org/')
        ip = response.text.strip()
        return ip
    except requests.RequestException:
        print('Unable to get remote ip. Please enter it manually.')
        remote_ip = input('Enter the remote ip: ')
        return remote_ip


# With the certificate and key contents, generate the client configuration file
def gen_client_cert():
    os.system('/etc/openvpn/easy-rsa/easyrsa build-client-full ' + get_client_name() + ' nopass')
    os.system('mkdir /etc/openvpn/server/clients/' + get_client_name())
    os.system('cp /etc/openvpn/easy-rsa/pki/ca.crt /etc/openvpn/server/clients/' + get_client_name() + '/')
    os.system('cp /etc/openvpn/easy-rsa/pki/issued/' + get_client_name() + '.crt /etc/openvpn/server/clients/' + get_client_name() + '/')
    os.system('cp /etc/openvpn/easy-rsa/pki/private/' + get_client_name() + '.key /etc/openvpn/server/clients/' + get_client_name() + '/')
    os.system('cp /etc/openvpn/server/ta.key /etc/openvpn/server/clients/' + get_client_name() + '/')


# Generate the client configuration file
def gen_client_conf():
    with open('/etc/openvpn/server/clients/' + get_client_name() + '/' + get_client_name() + '.conf', 'w') as f:
        f.write('client\n')
        f.write('dev tun\n')
        f.write('proto ' + get_proto() + '\n')
        f.write('remote ' + get_remote_ip() + ' ' + get_port() + '\n')
        f.write('resolv-retry infinite\n')
        f.write('nobind\n')
        f.write('persist-key\n')
        f.write('persist-tun\n')
        f.write('ca ca.crt\n')
        f.write('cert ' + get_client_name() + '.crt\n')
        f.write('key ' + get_client_name() + '.key\n')

        # read the contents of certificate and key files
        with open('/etc/openvpn/server/clients/' + get_client_name() + '/ca.crt', 'r') as file:
            ca = file.read()
        with open('/etc/openvpn/server/clients/' + get_client_name() + '/' + get_client_name() + '.crt', 'r') as file:
            cert = file.read()
        with open('/etc/openvpn/server/clients/' + get_client_name() + '/' + get_client_name() + '.key', 'r') as file:
            key = file.read()
        with open('/etc/openvpn/server/clients/' + get_client_name() + '/ta.key', 'r') as file:
            ta = file.read()

        # write the contents of certificate and key files to client configuration file
        f.write(ca)
        f.write(cert)
        f.write(key)
        f.write(ta)
        f.write('key-direction 1\n')
        f.write('cipher AES-256-CBC\n')
        f.write('comp-lzo\n')
        f.write('verb 3\n')
        f.write('mute 20\n')
        f.close()
        # Move the client configuration file to the client directory
        os.system('mv /etc/openvpn/server/clients/' + get_client_name() + '/' + get_client_name() + '.conf /etc/openvpn/server/clients/' + get_client_name() + '/' + get_client_name() + '.ovpn')


# Create the client configuration file
def create_client_conf_dir_file():
    os.system('touch /etc/openvpn/server/ccd/' + get_client_name())
    with open('/etc/openvpn/server/ccd/' + get_client_name(), 'w') as f:
        f.write('iroute ' + get_client_subnet() + '\n')
        f.close()
    os.system('systemctl restart openvpn@server')


# Main function
def main():
    gen_client_cert()
    gen_client_conf()
    create_client_conf_dir_file()
    print('Client configuration file created successfully.')
    print('Client configuration file path: /etc/openvpn/server/clients/' + get_client_name() + '/' + get_client_name() + '.ovpn')


if __name__ == '__main__':
    main()
