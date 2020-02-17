#!/usr/bin/python3
import os
import subprocess
from urllib import parse
from urllib import request
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIRECTORY = 'templates'


def generate_configs():
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY), autoescape=select_autoescape(['xml']))
    for template_name in os.listdir(TEMPLATE_DIRECTORY):
        t = env.get_template(template_name)
        with open('conf/' + template_name, 'w') as conf:
            conf.write(t.render(https_enabled=ssl_certificates_provided(), auth_enabled=auth_credentials_provided()))


def download_trial_war():
    print('Downloading jpedal trial...')
    token = os.environ['TOKEN']
    url = 'https://files.idrsolutions.com/dl/jpedal/trial/jpedal-microservice.war?token=' + token
    with request.urlopen(url) as response:
        handle_response(response)


def download_full_war(url):
    username = os.environ['LICENSE_USERNAME']
    password = os.environ['LICENSE_PASSWORD']
    data = parse.urlencode({'username': username, 'password': password}).encode('ascii')
    with request.urlopen(url, data) as response:
        handle_response(response)


def handle_response(response):
    if response.status == 200:
        with open('/usr/local/tomcat/webapps/ROOT.war', 'wb') as f:
            f.write(response.read())
        print('Download successful')
    else:
        print('Download failed')
        print(response.read().decode())


def download_jpedal():
    print('Downloading jpedal...')
    download_full_war('https://files.idrsolutions.com/dl/jpedal/full/jpedal-microservice.war')

def is_trial():
    return 'TOKEN' in os.environ


def is_full():
    return all(x in os.environ for x in ['LICENSE_USERNAME', 'LICENSE_PASSWORD', 'PRODUCT'])


def new_war_required():
    return ('REDOWNLOAD' in os.environ) or not war_exists()


def war_exists():
    return os.path.isfile('/usr/local/tomcat/webapps/ROOT.war')


def ssl_certificates_provided():
    ssl_dir = '/opt/ssl/'
    ssl_files = [ssl_dir + filename for filename in ['certificate.crt', 'private.key', 'ca_bundle.crt']]
    return all(map(os.path.isfile, ssl_files))


def auth_credentials_provided():
    return all(x in os.environ for x in ['ACCESS_USERNAME', 'ACCESS_PASSWORD'])


if new_war_required():
    if is_trial() and is_full():
        print('Mixing trial TOKENs and full-version LICENSE_USERNAME/LICENSE_PASSWORD combination is not supported.')
        print('If you have purchased a license, please remove the TOKEN argument to use the full version.')
        print('If you wish to trial jpedal, please remove any LICENSE_USERNAME, LICENSE_PASSWORD or PRODUCT argument.')
        exit(2)
    elif is_full():
        product = os.environ['PRODUCT'].lower()
        if product == 'jpedal':
            download_jpedal()
        else:
            print('Error: Unrecognised product "' + product + '".')
            print('Valid options are "jpedal".')
            exit(2)
    elif is_trial():
        download_trial_war()
    else:
        print('Please provide a valid trial token or username/password/product combination to download jpedal')

if war_exists():
    generate_configs()
    try:
        subprocess.run(['catalina.sh', 'run'], stdout=subprocess.PIPE, universal_newlines=True)
    except KeyboardInterrupt:
        exit()
else:
    print('Error: jpedal WAR file is missing.')
    exit(1)


