import requests
import os
import json
import time
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
while True:
    session = get_session(os.environ['clientId'],os.environ['tenantId'],os.environ['secret'],os.environ['username'],os.environ['password'])
    msgs = get_messages(session)
    num_msgs = len(msgs)
    #print(len(msgs))
    if num_msgs > 0:
        if num_msgs >= 1:
            for msg in msgs:
                resend_msg(session,msg,os.environ['to'])
                delete_msg(session,msg)
    session.close()
    time.sleep(2)
    del session
