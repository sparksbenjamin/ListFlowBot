from functions import *
from cmd import Cmd
class MyPrompt (Cmd):
    prompt = 'lfb> '
    intro = "Type ? to list commands"
    def do_exit(self, inp):
        return True
    def do_add(self, inp):
        print("adding '{}'".format(inp))
    
    def do_SetAzureAccess(self, inp):
        cid = input("Client ID:")
        tid = input("Tenant ID:")
        srt = input("API Secret:")
        setAzureAccess(tid,cid,srt)
        

    def help_SetAzureAccess(self):
        print('Sets Azure access tokens')
    
    def do_DisplayLists(self, inp):
        configs = load_config()
        for list in configs['lists'].values():
            #print(list['name'])
            print(json.dumps(list))
        
        
    def do_AddList(self, inp):
        name = input("List Name: ")
        uname = input("Username: ")
        secret = input("Password: ")
        to = input("Forward To: ")
        addList(name,uname,secret,to)
        

    def help_AddList(self):
        print('Adds New mailbox and forward to be watched')



if __name__ == '__main__':
    MyPrompt().cmdloop()

