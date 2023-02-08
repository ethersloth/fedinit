#!/bin/python3
import ipaddress
import os


def gen_cert_authority():
    try:
        os.system("openssl genpkey -algorithm RSA -out ca.key -aes256 -outform PEM -aes256 -nodes openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj '/C=US/ST=IL/L=East Alton/O=GregNet/OU=GregNet/emailAddress=gregory.allen.whitlock@gmail.com'")
        os.system("cp ca.crt /etc/openvpn/server/")
        os.system("cp ca.key /etc/openvpn/server/")
    except os.error as e:
        print(e.output)
        print('Error: Failed to generate certificate authority')
        return
    print('Success: Generated certificate authority')


def gen_server_cert():
    try:
        os.system("openssl req -new -key server.key -out server.csr")
        os.system("openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt")
    except os.error as e:
        print(e.output)
        print('Error: Failed to generate server certificate')
        return


def gen_dh_params():
    try:
        os.system("openssl dhparam -out dh2048.pem 2048")
    except os.error as e:
        print(e.output)
        print('Error: Failed to generate Diffie-Hellman parameters')
        return


def gen_tls_auth():
    try:
        os.system("openvpn --genkey --secret ta.key")
        os.system("cp ta.key /etc/openvpn/server/")
    except os.error as e:
        print(e.output)
        print('Error: Failed to generate TLS authentication key')
        return


# Ask user to enter the port number to use for OpenVPN and validate the input
def get_port():
    port = input('Enter the port number to use for OpenVPN: ')
    while not port.isdigit() or int(port) < 1 or int(port) > 65535:
        port = input('Invalid port number. Enter a valid port number: ')
    return port


def get_proto():
    proto = input('Enter the protocol to use for OpenVPN (tcp or udp): ')
    while proto != "tcp" and proto != "udp":
        proto = input('Invalid protocol. Enter a valid protocol (tcp or udp): ')
    return proto


# Ask user to enter subnet to use for OpenVPN and validate the input using ipaddress module
def get_server_subnet():
    subnet = input('Enter the subnet to use for OpenVPN (e.g.10.8.0.0 255.255.255.0): ')
    while not ipaddress.ip_network(subnet, strict=False):
        subnet = input('Invalid subnet. Enter a valid subnet (e.g.10.8.0.0 255.255.255.0): ')
    # Write Server subnet to file as Server Subnet x.x.x.x x.x.x.x
    with open('ip_subnet.txt', 'w') as f:
        f.write("Server:" + subnet)
        f.close()
    return subnet


def get_route():
    from openvpnclient import get_client_subnet
    # Make sure the client subnet is valid
    route = "route " + get_client_subnet()
    with open('server.conf', 'r+') as f:
        f.readlines()
        if route in f:
            print("Route already exists")
            return
        else:
            f.write(route)
            f.close()
    return route


def get_push_route():
    from openvpnclient import get_client_subnet
    push_route = "push \"route " + get_client_subnet() + "\""
    with open('server.conf', 'r+') as f:
        f.readlines()
        if push_route in f:
            print("Push route already exists")
            return
        else:
            f.write(push_route)
            f.close()
    return push_route


def gen_server_config():
    # File paths for the certificate and key files
    port = get_port()
    proto = get_proto()
    dev = "dev tun"
    ca_crt = "ca.crt"
    server_crt = "server.crt"
    server_key = "server.key"
    dh_pem = "dh.pem"
    ta_key = "ta.key"
    topology = "topology subnet"
    server = get_server_subnet()
    ifconfig_pool_persist = "ifconfig-pool-persist ipp.txt"
    client_to_client = "client-to-client"
    client_config_dir = "ccd"
    keepalive = "keepalive 10 120"
    cipher = "cipher AES-256-CBC"
    comp_lzo = "comp-lzo"
    persist_key = "persist-key"
    persist_tun = "persist-tun"
    status = "status openvpn-status.log"
    log = "log openvpn.log"
    log_append = "log openvpn.log"
    verb = "3"
    mute = "mute 20"
    explicit_exit_notify = "explicit-exit-notify"

    # Read the contents of the certificate and key files
    with open(ca_crt, 'r') as f:
        ca_crt = f.read()
    with open(server_crt, 'r') as f:
        server_crt = f.read()
    with open(server_key, 'r') as f:
        server_key = f.read()
    with open(dh_pem, 'r') as f:
        dh_pem = f.read()
    with open(ta_key, 'r') as f:
        ta_key = f.read()

    # Create a template for the OpenVPN configuration file
    template = """
    # OpenVPN Server Configuration
    port {port}
    proto {protocol}
    dev tun
    ca {ca_crt}
    cert {server_crt}
    key {server_key}
    dh {dh_pem}
    tls-auth {ta_key}
    topology subnet
    server {server}
    ifconfig-pool-persist ipp.txt
    push route {push_route}
    route {route}
    client-to-client
    client-config-dir ccd
    keepalive 10 120
    cipher AES-256-CBC
    comp-lzo
    persist-key
    persist-tun
    status openvpn-status.log
    log-append openvpn.log
    verb 3
    mute 20
    explicit-exit-notify 1
    
    """

    # Fill in the template with the contents of the certificate and key files
    config = template.format(port=port, protocol=proto, dev=dev, ca_crt=ca_crt, server_crt=server_crt, server_key=server_key, dh_pem=dh_pem, ta_key=ta_key, server=server, client_to_client=client_to_client, client_config_dir=client_config_dir, keepalive=keepalive, cipher=cipher, comp_lzo=comp_lzo, persist_key=persist_key, persist_tun=persist_tun, status=status, log=log, log_append=log_append, verb=verb, mute=mute, explicit_exit_notify=explicit_exit_notify, topology=topology, ifconfig_pool_persist=ifconfig_pool_persist)

    # Write the filled-in template to the OpenVPN configuration file
    with open("server.ovpn", "w") as f:
        f.write(config)
        f.close()
    print("OpenVPN configuration file created successfully")


def create_clients_dir():
    os.system("mkdir /etc/openvpn/server/clients")
    print("Clients directory created successfully")


def create_ccd_dir():
    os.system("mkdir /etc/openvpn/server/ccd")
    print("ccd directory created successfully")


def create_ipp_file():
    os.system("touch /etc/openvpn/server/ipp.txt")
    print("ipp.txt file created successfully")


def create_openvpn_status_file():
    os.system("touch /etc/openvpn/server/openvpn-status.log")
    print("openvpn-status.log file created successfully")


def create_openvpn_log_file():
    os.system("touch /etc/openvpn/server/openvpn.log")
    print("openvpn.log file created successfully")


def main():
    create_clients_dir()
    create_ccd_dir()
    create_ipp_file()
    create_openvpn_status_file()
    create_openvpn_log_file()
    gen_server_config()
    get_route()
    get_push_route()
    print("OpenVPN server configuration complete")
    os.system("systemctl enable openvpn")
    os.system("systemctl start openvpn")
    os.system("/bin/python3 openvpnclient.py")


if __name__ == "__main__":
    main()
