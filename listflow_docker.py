import requests
import os
import json
import time
import decimal

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
def get_messages(session):
    messages = session.get('https://graph.microsoft.com/v1.0/me/messages')
    messages = json.loads(messages.text)
    return messages['value']
def resend_msg(session,msg,to):
    fw_msg = {
        "message": {
            "subject": msg['subject'],
            "replyTo": [
                {
                    "emailAddress":{
                        "address": msg['from']
                    }
                }
            ],
            "body": {
                "contentType": msg['body']['contentType'],
                "content": msg['body']['content']
            },
            "bccRecipients": [
                {
                    "emailAddress": {
                    "address": to
                    }
                }
            ],
            "replyTo": msg['from']
            
        },
        "saveToSentItems": "false"
    }
    rp = session.post('https://graph.microsoft.com/v1.0/me/sendmail', json=fw_msg)
    if rp.status_code != 202:
        print(json.dumps(fw_msg))
        exit('Failed to Send Message ' + msg['id'])
def delete_msg(session,msg):
    del_url = 'https://graph.microsoft.com/v1.0/me/messages/'+ msg['id']
    del_rp = session.delete(del_url)
    time.sleep(5)
    if del_rp.status_code != 204:
        print(del_rp)
        exit('Failed to Delete Message ' + msg['id'])
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



_clientID = os.environ['clientId']
_tenantID = os.environ['tenantId']
_secret = os.environ['secret']
_username = os.environ['username']
_password = os.environ['password']
_to = os.environ['to']




while True:
    stime = decimal.Decimal(time.perf_counter())
    session = get_session(_clientID,_tenantID,_secret,_username,_password)
    
    msgs = get_messages(session)
    num_msgs = len(msgs)
    #print(len(msgs))
    if num_msgs > 0:
        if num_msgs >= 1:
            for msg in msgs:
                resend_msg(session,msg,_to)
                delete_msg(session,msg)
    session.close()
    etime = decimal.Decimal(time.perf_counter())
    ttime = etime - stime
    if ttime < 20:
        time.sleep(20)
    del session
    del ttime
    del etime
    del msgs
    del num_msgs