#!/bin/python3

import os
import subprocess
import platform

server_admin = 'admin@example.com'
server_name = 'example.com'
document_root = '/var/www/html'
APACHE_LOG_DIR = '/var/log/apache2'

# Check if we are running as root
if os.geteuid() != 0:
    raise Exception('Error: Must be run as root')


# Get server_admin email address, server_name, document_root, and APACHE_LOG_DIR
def get_server_admin():
    global server_admin
    global server_name
    global document_root
    global APACHE_LOG_DIR
    server_admin = input('Enter server_admin email address: ')
    # Validate server_admin email address
    while not server_admin.isalnum():
        server_admin = input('Invalid email address. Enter a valid email address: ')
        # should contain @ and end with .com/.net/.org/.edu/.gov/.mil/.int/.arpa/.biz/.info/.name/.pro/.aero/.coop/.museum/.travel/.xxx/.idv/.mobi/.asia/.cat/.jobs/.tel/.xxx/.me/.tv/.cc/.ws/.bz/.us/.uk/.ca/.eu/.de/.jp/.fr/.au/.ru/.nl/.it/.cn/.es/.se/.no/.co.uk/.org.uk/.me.uk/.mx/.co.nz/.net.nz/.org.nz/.co.za/.net.za/.org.za/.co.in/.net.in/.org.in/.in/.co.id/.net.id/.org.id/.ac.id/.sch.id/.web.id/.my/.com.my/.net.my/.org.my/.edu.my/.gov.my/.sg/.com.sg/.net.sg/.org.sg/.edu.sg/.gov.sg/.com.hk/.net.hk/.org.hk/.edu.hk/.gov.hk/.tw/.com.tw/.net.tw/.org.tw/.edu.tw/.gov.tw/.hk/.com.hk/.net.hk/.org.hk/.edu.hk/.gov.hk/.kr/.co.kr/.ne.kr/.or.kr/.pe.kr/.re.kr/.se.kr/.mil.kr/.go.kr/.ms.kr/.ac.kr/.hs.kr/.kg.kr/.es.kr/.sc.kr/.busan.kr/.daegu.kr/.daejeon.kr/.gangwon.kr/.gwangju.kr/.gyeonggi.kr/.incheon.kr/.jeju.kr/.jeonbuk.kr/.jeonnam.kr/.seoul.kr/.ulsan.kr/.chungbuk.kr/.chungnam.kr/.gyeongbuk.kr/.gyeongnam.kr/.jeonbuk.kr/.jeonnam.kr/.chungnam.kr/.gyeongbuk.kr/.gyeongnam.kr/.kw.kr/.ky.kr/.cn/.com.cn/.net.cn/.org.cn/.edu.cn/.gov.cn/.ah.cn/.bj.cn/.cq.cn/.fj.cn/.gd.cn/.gs.cn/.gz.cn/.gx.cn/.ha.cn/.hb.cn/.he.cn/.hi.cn/.hl.cn/.hn.cn/.jl.cn/.js.cn/.jx.cn/.ln.cn/.nm.cn/.nx.cn/.qh.cn/.sc.cn/.sd.cn/.sh.cn/.sn.cn/.sx.cn/.tj.cn/.xj.cn/.xz.cn/.yn
        if server_admin.find('@') == -1:
            server_admin = input('Invalid email address. Enter a valid email address: ')
        elif server_admin.endswith('.com') or server_admin.endswith('.net') or server_admin.endswith(
                '.org') or server_admin.endswith('.edu') or server_admin.endswith('.gov') or server_admin.endswith(
                '.mil') or server_admin.endswith('.int') or server_admin.endswith('.arpa') or server_admin.endswith(
                '.biz') or server_admin.endswith('.info') or server_admin.endswith('.name') or server_admin.endswith(
                '.pro') or server_admin.endswith('.aero') or server_admin.endswith('.coop') or server_admin.endswith(
                '.museum') or server_admin.endswith('.travel') or server_admin.endswith(
                '.xxx') or server_admin.endswith('.idv') or server_admin.endswith('.mobi') or server_admin.endswith(
                '.asia') or server_admin.endswith('.cat') or server_admin.endswith('.jobs') or server_admin.endswith(
                '.tel') or server_admin.endswith('.xxx') or server_admin.endswith('.me') or server_admin.endswith(
                '.tv') or server_admin.endswith('.cc') or server_admin.endswith('.ws') or server_admin.endswith(
                '.bz') or server_admin.endswith('.us') or server_admin.endswith('.uk') or server_admin.endswith(
                '.ca') or server_admin.endswith('.eu') or server_admin.endswith('.de') or server_admin.endswith(
                '.jp') or server_admin.endswith('.fr') or server_admin.endswith('.au') or server_admin.endswith(
                '.ru') or server_admin.endswith('.nl') or server_admin.endswith('.it') or server_admin.endswith(
                '.cn') or server_admin.endswith('.es') or server_admin.endswith('.se') or server_admin.endswith(
                '.no') or server_admin.endswith('.co.uk') or server_admin.endswith('.org.uk') or server_admin.endswith(
                '.me.uk') or server_admin.endswith('.mx') or server_admin.endswith('.co.nz') or server_admin.endswith(
                '.net.nz') or server_admin.endswith('.org.nz') or server_admin.endswith(
                '.co.za') or server_admin.endswith('.net.za') or server_admin.endswith(
                '.org.za') or server_admin.endswith('.co.in') or server_admin.endswith(
                '.net.in') or server_admin.endswith('.org.in') or server_admin.endswith('.in') or server_admin.endswith(
                '.co.id') or server_admin.endswith('.net.id') or server_admin.endswith(
                '.org.id') or server_admin.endswith('.ac.id') or server_admin.endswith(
                '.sch.id') or server_admin.endswith('.web.id') or server_admin.endswith('.my') or server_admin.endswith(
                '.com.my') or server_admin.endswith('.net.my') or server_admin.endswith(
                '.org.my') or server_admin.endswith('.edu.my') or server_admin.endswith(
                '.gov') or server_admin.endswith('.mil') or server_admin.endswith('.int') or server_admin.endswith(
                '.arpa') or server_admin.endswith('.biz') or server_admin.endswith('.info') or server_admin.endswith(
                '.name') or server_admin.endswith('.pro') or server_admin.endswith('.aero') or server_admin.endswith(
                '.coop') or server_admin.endswith('.museum') or server_admin.endswith(
                '.travel') or server_admin.endswith('.xxx') or server_admin.endswith('.idv') or server_admin.endswith(
                '.mobi') or server_admin.endswith('.asia') or server_admin.endswith('.cat') or server_admin.endswith(
                '.jobs') or server_admin.endswith('.tel') or server_admin.endswith('.xxx') or server_admin.endswith(
                '.me') or server_admin.endswith('.tv') or server_admin.endswith('.cc') or server_admin.endswith(
                '.ws') or server_admin.endswith('.bz') or server_admin.endswith('.us') or server_admin.endswith(
                '.uk') or server_admin.endswith('.ca') or server_admin.endswith('.eu') or server_admin.endswith(
                '.de') or server_admin.endswith('.jp') or server_admin.endswith('.fr') or server_admin.endswith(
                '.au') or server_admin.endswith('.ru') or server_admin.endswith('.nl') or server_admin.endswith(
                '.it') or server_admin.endswith('.cn') or server_admin.endswith('.es') or server_admin.endswith(
                '.se') or server_admin.endswith('.no') or server_admin.endswith('.co.uk') or server_admin.endswith(
                '.org.uk') or server_admin.endswith('.me.uk') or server_admin.endswith('.mx') or server_admin.endswith(
                '.co.nz') or server_admin.endswith('.net.nz') or server_admin.endswith(
                '.org.nz') or server_admin.endswith('.co.za') or server_admin.endswith(
                '.net.za') or server_admin.endswith('.org.za') or server_admin.endswith(
                '.co.in') or server_admin.endswith('.net.in') or server_admin.endswith(
                '.org.in') or server_admin.endswith('.in') or server_admin.endswith('.co.id') or server_admin.endswith(
                '.net.id') or server_admin.endswith('.org.id') or server_admin.endswith(
                '.ac.id') or server_admin.endswith('.sch.id') or server_admin.endswith(
                '.web.id') or server_admin.endswith('.my') or server_admin.endswith('.com.my') or server_admin.endswith(
                '.net.my') or server_admin.endswith('.org.my') or server_admin.endswith(
                '.edu.my') or server_admin.endswith('.gov') or server_admin.endswith('.mil') or server_admin.endswith(
                '.int') or server_admin.endswith('#'):
            server_admin = input('Invalid server_admin. Enter a valid server_admin:')

    server_name = input('Enter server_name: ')
    # Validate the server_name
    while not server_name.isalnum():
        server_name = input('Invalid server_name. Enter a valid server_name:')

    document_root = input('Enter document_root: ')
    # Validate the document_root
    if os.path.isdir(document_root):
        pass
    else:
        print('Invalid document_root. Please enter a valid document_root.')
        document_root = input('Enter document_root: ')

    APACHE_LOG_DIR = input('Enter APACHE_LOG_DIR: ')
    # Validate the APACHE_LOG_DIR
    if os.path.isdir(APACHE_LOG_DIR):
        pass
    else:
        print('Invalid APACHE_LOG_DIR. Please enter a valid APACHE_LOG_DIR.')
        APACHE_LOG_DIR = input('Enter APACHE_LOG_DIR: ')

    return server_admin, server_name, document_root, APACHE_LOG_DIR


# See if we are running on RHEL/CentOS/Fedora/Rocky or Debian/Ubuntu
def get_os():
    lin_os = platform.system()
    if lin_os == 'Linux':
        distro = platform.linux_distribution()
        if distro[0] == 'CentOS' or distro[0] == 'Red Hat Enterprise Linux' or distro[0] == 'Fedora' or distro[0] == 'Rocky':
            return 'rhel'
        elif distro[0] == 'Ubuntu' or distro[0] == 'Debian':
            return 'debian'
        else:
            raise Exception(f'Error: {distro[0]} is not supported')
    else:
        raise Exception(f'Error: {lin_os} is not supported')


def download_nextcloud():
    os.system("wget -N https://download.nextcloud.com/server/releases/latest.zip -O latest.zip")


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f'Error: {stderr.decode()}')
    return stdout.decode()


# Run the commands for Debian/Ubuntu
def debian_commands():
    run_command('apt update')
    run_command('apt upgrade -y')
    run_command('apt install apache2 mariadb-server libapache2-mod-php7.4 -y')
    run_command('apt install php7.4-gd php7.4-json php7.4-mysql php7.4-curl php7.4-mbstring -y')
    run_command('mysql_secure_installation')
    run_command('mysql -u root -e "CREATE DATABASE nextcloud;"')
    run_command('mysql -u root -e "CREATE USER \'nextcloud\'@\'localhost\' IDENTIFIED BY \'password\';"')
    run_command('mysql -u root -e "GRANT ALL ON nextcloud.* TO \'nextcloud\'@\'localhost\';"')
    run_command('mysql -u root -e "FLUSH PRIVILEGES;"')
    run_command('unzip latest.zip')
    run_command('mv nextcloud /var/www/html/')
    run_command('chown -R www-data:www-data /var/www/html/nextcloud/')
    run_command('chmod 775 /var/www/html/nextcloud/')
    run_command('touch /etc/apache2/sites-available/nextcloud.conf')
    create_nextcloud_conf_debian()
    run_command('a2ensite nextcloud.conf')
    run_command('systemctl restart apache2')


# Run the commands for RHEL/CentOS/Fedora/Rocky
def rhel_commands():
    run_command('dnf update -y')
    run_command('dnf install httpd mariadb-server php php-gd php-json php-mysqlnd php-curl php-mbstring -y')
    run_command('mysql_secure_installation')
    run_command('mysql -u root -e "CREATE DATABASE nextcloud;"')
    run_command("mysql -u root -e \"CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY 'password';\"")
    run_command("mysql -u root -e \"GRANT ALL ON nextcloud.* TO 'nextcloud'@'localhost';\"")
    run_command('mysql -u root -e "FLUSH PRIVILEGES;"')
    run_command('unzip latest.zip')
    run_command('mv nextcloud /var/www/html/')
    run_command('chown -R apache:apache /var/www/html/nextcloud/')
    run_command('chmod 775 /var/www/html/nextcloud/')
    run_command('touch /etc/httpd/conf.d/nextcloud.conf')
    create_nextcloud_conf_rhel()
    run_command('systemctl restart httpd')


def create_nextcloud_conf_debian():
    global server_admin, server_name, document_root, APACHE_LOG_DIR
    nextcloud_conf = f"""<VirtualHost *:80>
    ServerAdmin {server_admin}
    ServerName {server_name}
    DocumentRoot {document_root}

    <Directory {document_root}>
        Options +FollowSymlinks
        AllowOverride All
        Require all granted
        <IfModule mod_dav.c>
            Dav off
        </IfModule>
        SetEnv HOME {document_root}
        SetEnv HTTP_HOME {document_root}
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
    """
    with open("/etc/apache2/sites-available/nextcloud.conf", "w") as file:
        file.write(nextcloud_conf)


def create_nextcloud_conf_rhel():
    global server_admin, server_name, document_root, APACHE_LOG_DIR
    nextcloud_conf = f"""<VirtualHost *:80>
    ServerAdmin {server_admin}
    ServerName {server_name}
    DocumentRoot {document_root}

    <Directory {document_root}>
        Options +FollowSymlinks
        AllowOverride All
        Require all granted
        <IfModule mod_dav.c>
            Dav off
        </IfModule>
        SetEnv HOME {document_root}
        SetEnv HTTP_HOME {document_root}
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
    """
    with open("/etc/httpd/conf.d/nextcloud.conf", "w") as file:
        file.write(nextcloud_conf)


def main():
    global server_admin, server_name, document_root, APACHE_LOG_DIR
    server_admin, server_name, document_root, APACHE_LOG_DIR = get_server_admin()
    lin_os = get_os()
    download_nextcloud()
    if lin_os == 'debian':
        debian_commands()
    elif lin_os == 'rhel':
        rhel_commands()


if __name__ == '__main__':
    main()

