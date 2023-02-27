import json
from os.path import exists
import imaplib
import requests
import threading
import concurrent.futures
import time
from decimal import Decimal
import sys


pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
config_file_path = "main.conf"
running = True
def setAzureAccess(tenantID,ClientID,Secret):
    configs = load_config()
    configs['tenantId'] = tenantID
    configs['clientID'] = ClientID
    configs['secret'] = Secret
    save_config(configs)

def addList(list_name,mailbox_username,mailbox_password,mailbox_fwd_address):
    configs = load_config()
    lists = dict(configs['lists'])
    num = len(lists)
    num = str(num)
    nlist = { num : {
            "name": list_name,
            "username": mailbox_username,
            "password": mailbox_password,
            "to": mailbox_fwd_address
                }
            }
    lists.update(nlist)
    configs['lists'] = lists
    #print(configs)
    save_config(configs)
    


def mb_watch(list,configs):
    #print('[][+] Starting Sesstion')
    session = get_session(configs['clientId'],configs['tenantId'],configs['secret'],list['username'],list['password'])
    process_mailbox(session,list)
    #print('[][+] Closing Sesstion')
    session.close()
    time.sleep(2)
    del session
def resend_msg(session,msg,list):
    fw_msg = {
        "message": {
            "subject": msg['subject'],
            "body": {
                "contentType": msg['body']['contentType'],
                "content": msg['body']['content']
            },
            "bccRecipients": [
                {
                    "emailAddress": {
                    "address": list['to']
                    }
                }
            ]
        },
        "saveToSentItems": "false"
    }
    rp = session.post('https://graph.microsoft.com/v1.0/me/sendmail', json=fw_msg)
    if rp.status_code != 202:
        exit('Failed to Send Message ' + msg['id'])

def delete_msg(session,msg):
    del_url = 'https://graph.microsoft.com/v1.0/me/messages/'+ msg['id']
    del_rp = session.delete(del_url)
    time.sleep(5)
    if del_rp.status_code != 204:
        print(del_rp)
        exit('Failed to Delete Message ' + msg['id'])
def get_messages(session):
    messages = session.get('https://graph.microsoft.com/v1.0/me/messages')
    messages = json.loads(messages.text)
    return messages['value']
def get_session(client,tenat,secret,username,password):
    session = requests.session()
    token_url = 'https://login.microsoftonline.com/' + tenat + '/oauth2/token'
    token_data = {
        'grant_type': 'password',
        'client_id': client,
        'client_secret': secret,
        'resource': 'https://graph.microsoft.com',
        'scope':'https://graph.microsoft.com',
        'username':username,
        'password':password,
        }
    token_r = session.post(token_url, data=token_data)
    token = token_r.json().get('access_token')
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    session.headers = headers
    return session
def process_mailbox(session,list):
    msgs = get_messages(session)
    num_msgs = len(msgs)
    #print(len(msgs))
    if num_msgs > 0:
        if num_msgs >= 1:
            for msg in msgs:
                resend_msg(session,msg,list)
                delete_msg(session,msg)
    del msgs
def save_config(config):
    with open(config_file_path,'w',encoding='utf-8') as outfile:
        json.dump(config, outfile, ensure_ascii=False, indent=4)
def load_config():
    
    # Check for file exists
    file_exists = exists(config_file_path)
    if file_exists:
        with open(config_file_path) as config_file:
            file_contents = config_file.read()    
        lists_config = json.loads(file_contents)
        
        return lists_config
    else:
        print('Error: Config File Missing')
        exit(100)

#EOF