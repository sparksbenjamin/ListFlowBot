import requests
import os
import json
import time
import decimal
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
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
def msg_json_encode(msg,to):
    fw_msg = {
        "message": {
            "subject": msg['subject'],
            "replyTo": [
                {
                    "emailAddress":{
                        "address": msg['sender']['emailAddress']['address']
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
        },
        "saveToSentItems": "false"
    }
    return fw_msg
def msg_mime_encode(msg,to):

    body = msg['body']
    efrom = msg['sender']['emailAddress']['address']
    print(json.dumps(efrom))
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    emsg = MIMEMultipart()
    emsg['replyTo'] = efrom
    emsg['subject'] = msg['subject']
    emsg['bccRecipients'] = to
    emsg['body'] = msg['body']
    enc
    return emsg
def resend_msg(session,msg,to):
    new_msg = msg_json_encode(msg,to)
    #new_msg = msg_mime_encode(msg,to)
    #encodedbytes = base64.b64encode(new_msg)
    #print(encodedbytes)
    #print(json.dumps(new_msg))
    #exit
    rp = session.post('https://graph.microsoft.com/v1.0/me/sendmail', json=new_msg)
    #rp = session.post('https://graph.microsoft.com/v1.0/me/sendmail', file=new_msg )
    if rp.status_code != 202:
        #print(json.dumps(fw_msg))
        print("ERROR: Failed to Send Message " + msg['id'])
        #exit('Failed to Send Message ' + msg['id'])
    else:
        print("Message forwarded to " + to)
        delete_msg(session,msg)
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
                #delete_msg(session,msg)
    del msgs

_vars_set_ = False
_clientID = ""
_tenantID = ""
_secret = ""
_username = ""
_password = ""
_to = ""

try:
    _clientID = os.environ['clientId']
    _tenantID = os.environ['tenantId']
    _secret = os.environ['secret']
    _username = os.environ['username']
    _password = os.environ['password']
    _to = os.environ['to']
    _vars_set_ = True
except:
    print("[!] Error: Options not set")
    if _clientID == "":
            print("[!-->} No clientID set")
            _running_ = False
    if _tenantID == "":
            print("[!-->} No TenantID set")
            _running_ = False



while True:
    if _vars_set_:
        stime = decimal.Decimal(time.perf_counter())
        session = get_session(_clientID,_tenantID,_secret,_username,_password)
        
        msgs = get_messages(session)
        num_msgs = len(msgs)
        #print(len(msgs))
        if num_msgs > 0:
            if num_msgs >= 1:
                for msg in msgs:
                    resend_msg(session,msg,_to)
                    #delete_msg(session,msg)
        session.close()
        etime = decimal.Decimal(time.perf_counter())
        ttime = etime - stime
        print("Process Mailbox in " + ttime)
        if ttime < 20:
            time.sleep(20)
        del session
        del ttime
        del etime
        del msgs
        del num_msgs
    else:
        print("[!] Error Please set variables")
        time.sleep(300)