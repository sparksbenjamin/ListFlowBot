# ListFlowBot
---
> Powered by the python and [["Microsoft Graph API"](https://learn.microsoft.com/en-us/graph/overview)]
---
This a catch and release system.  It watches a shared mailbox and resends the email to a email address including a Office 365 group or DL.  Mail flow logs will stay within Office 365 along with all access rules. 

## Purpose
To provide ListServe features to [["Microsoft Office 365"]()].  With this service it will check the mailbox and resend any messages as it's self to the email address provided. 

## Useage

## Setup
There are a few steps to complete to get this system running.  You will need to create an Application in Azure AD and provide it API access and get the keys.  

### Azure Setup
Add to Azure for GraphAPI access https://learn.microsoft.com/en-us/graph/tutorials/python?tabs=aad&tutorial-step=1

### System Setup

#### Install

Download the latest version

```
sudo apt install python3 git
git clone https://github.com/sparksbenjamin/ListFlowBot
cd ListFlowBot
chmod +x install.sh
sudo ./install.sh
```

### Lists Setup
A lists is a combination of a Front Facing mailbox and group to send the messages to.  You can restrict who can send to mailbox using any of your other means.  All of your Mail restrictions provided by o365 are still in effect and this system does not attempt to work around them. 


## Donate
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sparksbenjamin)
---
>All development projects are fueled by personal time and caffine.  If you feel so inclinded please feel free to buy a cup. 
---


