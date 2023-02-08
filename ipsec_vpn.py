#!/bin/python3
# Using StrongSwan to create an IPsec VPN server
import getpass
import ipaddress
import shutil

import requests
from OpenSSL import crypto

tunnel_name = 'tunnel'
tunnel_names = []
tunnel_type = 'server'
negotiation_mode = 'main'
dpd_action = 'enable'
dpd_interval = '30'
dpd_timeout = '60'
pfs = 'enable'
ike_version = 'ikev2'
ike_fragmentation = 'yes'
p1_encryption_algorithm = 'AES-256'
p1_auth_type = 'SHA2-256'
p1_dh_group = 'Group 14'
p1_lifetime = '28800'
encryption_method = 'psk'
psk = '20PreSharedKey22'
certificates = 'n/a'
local_peer_id = 'n/a'
remote_peer_id = 'n/a'
p2_auth_type = 'esp'
p2_ah_authentication = 'n/a'
p2_encryption_algorithm = 'aes256'
p2_authentication = 'sha1'
p2_dh_group = 'Group 14'
p2_sa_lifetime = '3600'
local_public_ip = 'n/a'
local_source_ip = 'n/a'
local_gateway_ip = 'n/a'
local_private_subnets = []
remote_public_ip = 'n/a'
remote_source_ip = 'n/a'
remote_gateway_ip = 'n/a'
remote_private_subnets = []
client_name = 'n/a'
client_names = []
vpn_server_key = 'n/a'
vpn_server_cert = 'n/a'
client_cert = []
client_key = []


# Ask user what tunnel type they want to create (Server or Client)
def get_tunnel_type():
    global tunnel_type
    tunnel_type = input('Enter the tunnel type (Server or Client): ')
    while tunnel_type.lower() not in ['server', 'client']:
        tunnel_type = input('Invalid tunnel type. Enter a valid tunnel type (Server or Client): ')
    return tunnel_type


# If tunnel type is server, ask user what tunnel name they want to use, if tunnel name is empty, use default name
# if tunnel type is client, ask user what tunnel name they want to use
def get_tunnel_name():
    global tunnel_name
    if tunnel_name == 'tunnel':
        tunnel_name = input('Enter the tunnel name (Default: tunnel): ')
        if tunnel_type.lower() == 'server':
            while tunnel_name in tunnel_names:
                tunnel_name = tunnel_name + '1'
                tunnel_names.append(tunnel_name)
        if tunnel_name == '':
            tunnel_name = 'tunnel'
    elif tunnel_type.lower() == 'client':
        tunnel_name = input('Enter the tunnel name: ')
        while tunnel_name in tunnel_names:
            tunnel_name = tunnel_name + '1'
            tunnel_names.append(tunnel_name)
    return tunnel_name


# If tunnel type is server, ask user what Ike version they want to use
def get_ike_version():
    global ike_version
    ike_version = input('Enter the IKE version (1 or 2): ')
    while ike_version not in ['1', '2']:
        ike_version = input('Invalid IKE version. Enter a valid IKE version (1 or 2): ')
    if ike_version == '1':
        ike_version = 'ikev1'
    else:
        ike_version = 'ikev2'
        get_ike_fragmentation()
    return ike_version


# If tunnel type is server, and IKE version is 2, set Ike Fragmentation to yes
def get_ike_fragmentation():
    global ike_fragmentation
    ike_fragmentation = 'yes'
    return ike_fragmentation


# If tunnel type is server, ask user encryption method they want to use (PSK or Certificates)
def get_encryption_method():
    global encryption_method
    encryption_method = input('Enter the encryption method (PSK or Certificates): ')
    while encryption_method.lower() not in ['psk', 'certificates']:
        encryption_method = input('Invalid encryption method. Enter a valid encryption method (PSK or Certificates): ')
    return encryption_method


# If tunnel type is server and encryption method is PSK, ask user for PSK
def get_psk():
    global psk
    # psk = getpass.getpass('Enter the PSK: ')
    psk = getpass.getpass('Enter the PSK: ')
    while not psk.isalnum():
        psk = input('Invalid PSK. Enter a valid PSK: ')
    return psk


# Negotiation mode
def get_negotiation_mode():
    global negotiation_mode
    negotiation_mode = input('Enter the negotiation mode (main, aggressive): ')
    while negotiation_mode.lower() not in ['main', 'aggressive']:
        negotiation_mode = input('Invalid negotiation mode. Enter a valid negotiation mode (main, aggressive): ')
    return negotiation_mode


# DPD action Hold, Restart or disabled
def get_dpd_action():
    global dpd_action
    dpd_action = input('Enter the DPD action (hold, restart, disabled): ')
    while dpd_action.lower() not in ['hold', 'restart', 'disabled']:
        dpd_action = input('Invalid DPD action. Enter a valid DPD action (hold, restart, disabled): ')
    return dpd_action


# If DPD action is not disabled, ask user for DPD interval
def get_dpd_interval():
    global dpd_interval
    dpd_interval = input('Enter the DPD interval (in seconds): ')
    while not dpd_interval.isdigit():
        dpd_interval = input('Invalid DPD interval. Enter a valid DPD interval (in seconds): ')
    return dpd_interval


# If DPD action is not disabled, ask user for DPD timeout
def get_dpd_timeout():
    global dpd_timeout
    dpd_timeout = input('Enter the DPD timeout (in seconds): ')
    while not dpd_timeout.isdigit():
        dpd_timeout = input('Invalid DPD timeout. Enter a valid DPD timeout (in seconds): ')
    return dpd_timeout


# PFS Yes or No
def get_pfs():
    global pfs
    pfs = input('Enter the PFS (yes or no): ')
    while pfs.lower() not in ['yes', 'no']:
        pfs = input('Invalid PFS. Enter a valid PFS (yes or no): ')
    return pfs


# Phase 1 Authentication Type (MD5, SHA1, SHA256, SHA512)
def get_p1_auth_type():
    global p1_auth_type
    p1_auth_type = input('Enter the Phase 1 authentication type (MD5, SHA1, SHA256, SHA512): ')
    while p1_auth_type.lower() not in ['md5', 'sha1', 'sha256', 'sha512']:
        p1_auth_type = input(
            'Invalid Phase 1 authentication type. Enter a valid Phase 1 authentication type (MD5, SHA1, SHA256, SHA512): ')
    return p1_auth_type


# Phase 1 DH Group (1-768bits, 2-1024bits, 5-1536bits, 14-2048bits, 15-3072bits, 16-4096bits, 17-6144bits, 18-8192bits, 22-1024bits, 23-2048bits, 24-2048bits)
def get_p1_dh_group():
    global p1_dh_group
    p1_dh_group = input(
        'Enter the Phase 1 DH group (1-768bits, 2-1024bits, 5-1536bits, 14-2048bits, 15-3072bits, 16-4096bits, 17-6144bits, 18-8192bits, 22-1024bits, 23-2048bits, 24-2048bits): ')
    while p1_dh_group not in ['1', '2', '5', '14', '15', '16', '17', '18', '22', '23', '24']:
        p1_dh_group = input(
            'Invalid Phase 1 DH group. Enter a valid Phase 1 DH group (1-768bits, 2-1024bits, 5-1536bits, 14-2048bits, 15-3072bits, 16-4096bits, 17-6144bits, 18-8192bits, 22-1024bits, 23-2048bits, 24-2048bits): ')
    return p1_dh_group


# Phase 1 Encryption Algorithm (3DES, AES, AES128, AE256)
def get_p1_encryption_algorithm():
    global p1_encryption_algorithm
    p1_encryption_algorithm = input('Enter the Phase 1 encryption algorithm (3DES, AES, AES128, AES256): ')
    while p1_encryption_algorithm.lower() not in ['3des', 'aes', 'aes128', 'aes256']:
        p1_encryption_algorithm = input(
            'Invalid Phase 1 encryption algorithm. Enter a valid Phase 1 encryption algorithm (3DES, AES, AES128, AES256): ')
    return p1_encryption_algorithm


# Phase 2 Authentication Type (ESP or AH)
def get_p2_auth_type():
    global p2_auth_type
    p2_auth_type = input('Enter the Phase 2 authentication type (ESP or AH): ')
    while p2_auth_type.lower() not in ['esp', 'ah']:
        p2_auth_type = input(
            'Invalid Phase 2 authentication type. Enter a valid Phase 2 authentication type (ESP or AH): ')
    return p2_auth_type


# Get Phase 2 AH Authentication (hmac-md5-96 or hmac-sha1-96)
def get_p2_ah_authentication():
    global p2_ah_authentication
    p2_ah_authentication = input('Enter the Phase 2 AH authentication (hmac-md5-96 or hmac-sha1-96): ')
    while p2_ah_authentication.lower() not in ['hmac-md5-96', 'hmac-sha1-96']:
        p2_ah_authentication = input(
            'Invalid Phase 2 AH authentication. Enter a valid Phase 2 AH authentication (hmac-md5-96 or hmac-sha1-96): ')
    return p2_ah_authentication


# Phase 2 DH Group same as Phase 1
def get_p2_dh_group():
    global p2_dh_group
    p2_dh_group = p1_dh_group
    return p2_dh_group


# Phase 2 Authentication (MD5 or SHA1)
def get_p2_authentication():
    global p2_authentication
    p2_authentication = input('Enter the Phase 2 authentication (MD5 or SHA1): ')
    while p2_authentication.lower() not in ['md5', 'sha1']:
        p2_authentication = input(
            'Invalid Phase 2 authentication. Enter a valid Phase 2 authentication (MD5 or SHA1): ')
    return p2_authentication


# Phase 2 Encryption Algorithm (3DES, AES, AES128, AE256)
def get_p2_encryption_algorithm():
    global p2_encryption_algorithm
    p2_encryption_algorithm = input('Enter the Phase 2 encryption algorithm (3DES, AES, AES128, AES256): ')
    while p2_encryption_algorithm.lower() not in ['3des', 'aes', 'aes128', 'aes256']:
        p2_encryption_algorithm = input(
            'Invalid Phase 2 encryption algorithm. Enter a valid Phase 2 encryption algorithm (3DES, AES, AES128, AES256): ')
    return p2_encryption_algorithm


# Generate Certificates
def generate_certificates():
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    req = crypto.X509Req()
    req.get_subject().CN = "VPN Server"
    req.set_pubkey(key)
    req.sign(key, "sha256")
    cert = crypto.X509()
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(key, "sha256")
    with open("vpn-server-key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    with open("vpn-server-cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))


# Generate IPSec Client Certificates
def generate_client_certificates():
    # Generate Client Name
    global client_name
    client_name = input('Enter the client name: ')
    if client_name in client_names:
        client_name = client_name + str(client_names.count(client_name) + 1)
        generate_client_certificates()
    elif client_name == '':
        client_name = 'client1'

    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    req = crypto.X509Req()
    req.get_subject().CN = client_name
    req.set_pubkey(key)
    req.sign(key, "sha256")
    cert = crypto.X509()
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(key, "sha256")
    with open(client_name + "-key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    with open(client_name + "-cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))


# Move Certificates to /etc/ipsec.d/certs
def move_certificates():
    global client_name
    global vpn_server_key
    global vpn_server_cert
    global client_key
    global client_cert
    if encryption_method == 'cert':
        if tunnel_type == 'server':
            shutil.move('vpn-server-key.pem', '/etc/ipsec.d/private/vpn-server-key.pem')
            vpn_server_key = open('/etc/ipsec.d/private/vpn-server-key.pem', 'r')
            shutil.move('vpn-server-cert.pem', '/etc/ipsec.d/certs/vpn-server-cert.pem')
            vpn_server_cert = open('/etc/ipsec.d/certs/vpn-server-cert.pem', 'r')
            return vpn_server_key, vpn_server_cert
        elif tunnel_type == 'client':
            for client_name in client_name:
                shutil.move(client_name + '-key.pem', '/etc/ipsec.d/private/' + client_name + '-key.pem')
                client_key = open('/etc/ipsec.d/private/' + client_name + '-key.pem', 'r')
                shutil.move(client_name + '-cert.pem', '/etc/ipsec.d/certs/' + client_name + '-cert.pem')
                client_cert = open('/etc/ipsec.d/certs/' + client_name + '-cert.pem', 'r')
                client_key = client_key.append(str.format(client_key))
                client_cert = client_cert.append(str.format(client_cert))
            return client_key, client_cert


# Get Certs
def get_certs():
    global vpn_server_key
    global vpn_server_cert
    global client_key
    global client_cert
    vpn_server_key = move_certificates()[0]
    vpn_server_cert = move_certificates()[1]
    client_key = move_certificates()[2]
    client_cert = move_certificates()[3]
    return vpn_server_key, vpn_server_cert, client_key, client_cert


# Generate ipsec.secrets
def generate_ipsec_secrets():
    if tunnel_type == 'server':
        if encryption_method == 'psk':
            with open("ipsec.secrets", "w") as f:
                f.write(":%s : PSK \"%s\" # VPN Server PSK Secret)" % (tunnel_name, get_psk))
        elif encryption_method == 'cert':
            # ipsec secrets file will not need to be generated if using certificates
            pass

    elif tunnel_type == 'client':
        if encryption_method == 'psk':
            with open("ipsec.secrets", "w") as f:
                f.write("%s : PSK \"%s\" # VPN Client PSK Secret)" % (tunnel_name, get_psk))
        elif encryption_method == 'cert':
            # ipsec secrets file will not need to be generated if using certificates
            pass


# Get local public IP address, attempt to get public IP address from ipify.org
def get_public_ip():
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.exceptions.RequestException:
        public_ip = input('Unable to get public IP address. Enter public IP address: ')
        # Validate public IP address with ipaddress module
        while not ipaddress.ip_address(public_ip).is_global:
            public_ip = input('Invalid public IP address. Enter public IP address: ')
            # Validate public IP address with ipaddress module
            while not ipaddress.ip_address(public_ip).is_global:
                public_ip = input('Invalid public IP address. Enter public IP address: ')
    return public_ip


# Get Local Source IP Address
def get_source_ip():
    global local_source_ip
    local_source_ip = input('Enter the source IP address of the VPN server: ')
    # Validate source IP address with ipaddress module
    while not ipaddress.ip_address(local_source_ip).is_global:
        local_source_ip = input('Invalid source IP address. Enter source IP address: ')
        # Validate source IP address with ipaddress module
        while not ipaddress.ip_address(local_source_ip).is_global:
            local_source_ip = input('Invalid source IP address. Enter source IP address: ')
            # Validate source ip address is private with ipaddress module
            while not ipaddress.ip_address(local_source_ip).is_private:
                local_source_ip = input('Invalid source IP address. Enter source IP address: ')
    return local_source_ip


# Get Local Gateway IP Address
def get_gateway_ip():
    global local_gateway_ip
    local_gateway_ip = input('Enter the gateway IP address of the VPN server: ')
    # Validate gateway IP address with ipaddress module
    while not ipaddress.ip_address(local_gateway_ip).is_global:
        local_gateway_ip = input('Invalid gateway IP address. Enter gateway IP address: ')
        # Validate gateway IP address with ipaddress module
        while not ipaddress.ip_address(local_gateway_ip).is_global:
            local_gateway_ip = input('Invalid gateway IP address. Enter gateway IP address: ')
            # Validate gateway ip address is private with ipaddress module
            while not ipaddress.ip_address(local_gateway_ip).is_private:
                local_gateway_ip = input('Invalid gateway IP address. Enter gateway IP address: ')
    return local_gateway_ip


# Get Local Private Subnets recursively
def get_local_private_subnets():
    global local_private_subnets
    local_private_subnets = input('Enter the private subnets of the VPN server (Make sure to separate with comma): ')
    # Validate private subnet with ipaddress module
    while not ipaddress.ip_network(local_private_subnets).is_private:
        local_private_subnets = input('Invalid private subnet. Enter private subnet: ')
        # Validate private subnet with ipaddress module
        while not ipaddress.ip_network(local_private_subnets).is_private:
            local_private_subnets = input('Invalid private subnet. Enter private subnet: ')
    local_private_subnets = local_private_subnets.split(',')
    local_private_subnets = local_private_subnets.append(str.format(local_private_subnets))
    return local_private_subnets


# Get Remote Public IP Address
def get_remote_public_ip():
    global remote_public_ip
    remote_public_ip = input('Enter the public IP address of the VPN client: ')
    # Validate public IP address with ipaddress module
    while not ipaddress.ip_address(remote_public_ip).is_global:
        remote_public_ip = input('Invalid public IP address. Enter public IP address: ')
        # Validate public IP address with ipaddress module
        while not ipaddress.ip_address(remote_public_ip).is_global:
            remote_public_ip = input('Invalid public IP address. Enter public IP address: ')
    return remote_public_ip


# Get Remote Source IP Address
def get_remote_source_ip():
    global remote_source_ip
    remote_source_ip = input('Enter the source IP address of the VPN client: ')
    # Validate source IP address with ipaddress module
    while not ipaddress.ip_address(remote_source_ip).is_global:
        remote_source_ip = input('Invalid source IP address. Enter source IP address: ')
        # Validate source IP address with ipaddress module
        while not ipaddress.ip_address(remote_source_ip).is_global:
            remote_source_ip = input('Invalid source IP address. Enter source IP address: ')
            # Validate source ip address is private with ipaddress module
            while not ipaddress.ip_address(remote_source_ip).is_private:
                remote_source_ip = input('Invalid source IP address. Enter source IP address: ')
    return remote_source_ip


# Get Remote Gateway IP Address
def get_remote_gateway_ip():
    global remote_gateway_ip
    remote_gateway_ip = input('Enter the gateway IP address of the VPN client: ')
    # Validate gateway IP address with ipaddress module
    while not ipaddress.ip_address(remote_gateway_ip).is_global:
        remote_gateway_ip = input('Invalid gateway IP address. Enter gateway IP address: ')
        # Validate gateway IP address with ipaddress module
        while not ipaddress.ip_address(remote_gateway_ip).is_global:
            remote_gateway_ip = input('Invalid gateway IP address. Enter gateway IP address: ')
            # Validate gateway ip address is private with ipaddress module
            while not ipaddress.ip_address(remote_gateway_ip).is_private:
                remote_gateway_ip = input('Invalid gateway IP address. Enter gateway IP address: ')
    return remote_gateway_ip


# Get Remote Private Subnets recursively
def get_remote_private_subnets():
    global remote_private_subnets
    remote_private_subnets = input('Enter the private subnets of the VPN client (Make sure to separate by comma): ')
    # Validate private subnet with ipaddress module
    while not ipaddress.ip_network(remote_private_subnets).is_private:
        remote_private_subnets = input('Invalid private subnet. Enter private subnet: ')
        # Validate private subnet with ipaddress module
        while not ipaddress.ip_network(remote_private_subnets).is_private:
            remote_private_subnets = input('Invalid private subnet. Enter private subnet: ')
    remote_private_subnets = remote_private_subnets.split(',')
    remote_private_subnets = remote_private_subnets.append(str.format(remote_private_subnets))
    return remote_private_subnets


# Generate ipsec.conf based on ipsec.conf template
def generate_ipsec_conf():
    """
    conn {}.format(tunnel_name)
    fragmentation={}.format(fragmentation)
    dpdaction={}.format(dpdaction)
    ike={}-{}-{}.format(p1_encryption, p1_authentication, p1_dh_group)
    if p2_auth_type == 'ah':
        ah={}.format(p2_ah_authentication)
    elif p2_auth_type == 'esp':
        esp={}-{}-{}.format(p2_encryption, p2_authentication, p2_dh_group)
    keyingtries=%forever
    leftid={}.format(local_public_ip)
    if encryption_method == 'cert':
        leftcert={}.format(local_cert)
    elif encryption_method == 'psk':
        leftpsk={}.format(psk)
    else:
    conn {}.format(client_tunnel_name)
        exit(1)
        also={}.format(tunnel_name)
        keyexchange={}.format(ike_version)
        leftsubnet={}.format(local_private_subnets)
        leftsourceip={}.format(local_source_ip)
        leftgateway={}.format(local_gateway_ip)
        left={}.format(local_public_ip)
        right={}.format(remote_public_ip)
        rightsourceip={}.format(remote_source_ip)
        rightsubnet={}.format(remote_private_subnets)
        rightgateway={}.format(remote_gateway_ip)
        if encryption_method == 'cert':
            rightcert={}.format(remote_cert)
        elif encryption_method == 'psk':
            rightpsk={}.format(psk)
        else:
            exit(1)
    """

    # Create ipsec.conf file
    with open('ipsec.conf', 'w') as ipsec_conf:
        ipsec_conf.write('conn {}\n'.format(tunnel_name))
        ipsec_conf.write('fragmentation={}\n'.format(ike_fragmentation))
        ipsec_conf.write('dpdaction={}\n'.format(dpd_action))
        ipsec_conf.write('ike={}-{}-{}\n'.format(p1_encryption_algorithm, p1_auth_type, p1_dh_group))
        if p2_auth_type == 'ah':
            ipsec_conf.write('ah={}\n'.format(p2_ah_authentication))
        elif p2_auth_type == 'esp':
            ipsec_conf.write('esp={}-{}-{}\n'.format(p2_encryption_algorithm, p2_authentication, p2_dh_group))
        ipsec_conf.write('keyingtries=%forever\n')
        ipsec_conf.write('leftid={}\n'.format(local_public_ip))
        if encryption_method == 'cert':
            ipsec_conf.write('leftcert={}\n'.format(vpn_server_cert))
            ipsec_conf.write('leftkey={}\n'.format(vpn_server_key))
        elif encryption_method == 'psk':
            ipsec_conf.write('leftpsk={}\n'.format(psk))
        else:
            exit(1)
        for client in client_names:
            ipsec_conf.write('conn {}\n'.format(client))
            ipsec_conf.write('  also={}\n'.format(tunnel_name))
            ipsec_conf.write('  keyexchange={}\n'.format(ike_version))
            for ip in local_private_subnets:
                ipsec_conf.write('  leftsubnet={}\n'.format(ip))
            ipsec_conf.write('  leftsourceip={}\n'.format(local_source_ip))
            ipsec_conf.write('  leftgateway={}\n'.format(local_gateway_ip))
            ipsec_conf.write('  left={}\n'.format(local_public_ip))
            ipsec_conf.write('  right={}\n'.format(remote_public_ip))
            ipsec_conf.write('  rightsourceip={}\n'.format(remote_source_ip))
            for ip in remote_private_subnets:
                ipsec_conf.write('  rightsubnet={}\n'.format(ip))
            ipsec_conf.write('  rightgateway={}\n'.format(remote_gateway_ip))
            if encryption_method == 'cert':
                ipsec_conf.write('rightcert={}\n'.format(client_cert))
                ipsec_conf.write('rightkey={}\n'.format(client_key))
            elif encryption_method == 'psk':
                ipsec_conf.write('rightpsk={}\n'.format(psk))
            else:
                exit(1)
            ipsec_conf.write('  auto=route\n')


# Main function
def main():
    global vpn_server_key
    global vpn_server_cert
    get_tunnel_type()
    if tunnel_type == 'server':
        get_tunnel_name()
        get_encryption_method()
        if encryption_method == 'cert':
            get_certs()
        elif encryption_method == 'psk':
            get_psk()
        else:
            exit(1)
        get_ike_version()
        get_ike_fragmentation()
        get_dpd_action()
        get_p1_encryption_algorithm()
        get_p1_auth_type()
        get_p1_dh_group()
        get_p2_auth_type()
        if p2_auth_type == 'ah':
            get_p2_ah_authentication()
        elif p2_auth_type == 'esp':
            get_p2_encryption_algorithm()
            get_p2_authentication()
            get_p2_dh_group()
        else:
            exit(1)
        get_public_ip()
        get_local_private_subnets()
        get_source_ip()
        get_gateway_ip()
        get_remote_public_ip()
        get_remote_private_subnets()
        get_remote_source_ip()
        get_remote_gateway_ip()
        generate_ipsec_conf()
    elif tunnel_type == 'client':
        get_tunnel_name()
        get_encryption_method()
        if encryption_method == 'cert':
            get_certs()
        elif encryption_method == 'psk':
            get_psk()
        else:
            exit(1)
        get_ike_version()
        get_ike_fragmentation()
        get_dpd_action()
        get_p1_encryption_algorithm()
        get_p1_auth_type()
        get_p1_dh_group()
        get_p2_auth_type()
        if p2_auth_type == 'ah':
            get_p2_ah_authentication()
        elif p2_auth_type == 'esp':
            get_p2_encryption_algorithm()
            get_p2_authentication()
            get_p2_dh_group()
        else:
            exit(1)
        get_public_ip()
        get_local_private_subnets()
        get_source_ip()
        get_gateway_ip()
        get_remote_public_ip()
        get_remote_private_subnets()
        get_remote_source_ip()
        get_remote_gateway_ip()
        generate_ipsec_conf()
    else:
        exit(1)


if __name__ == '__main__':
    main()