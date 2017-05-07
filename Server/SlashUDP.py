import pip
import logging
from random import randint
import socket

logging.basicConfig(level=logging.INFO)

def install(package):
    pip.main(['install', package])

try:
    from profanity import profanity
except:
    install('profanity')
    from profanity import profanity

try:
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from chatterbot import ChatBot
except:
    install('chatterbot')
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from chatterbot import ChatBot

bot = ChatBot('Slash',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database='slash-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

cw = [line.rstrip('\n') for line in open('controversialwords.ini')]
profanity.load_words(cw)
NaziSymbol = "卐"

print("Started!")

UDP_PORT = 6754

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

def LoadShifting(server, data):
    SERVER_PORT = 3690
    OtherServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    OtherServerSock.bind(("", SERVER_PORT))
    data = "<key>#=&4afuRequfReTE+uTruRAPa</key>\n<data>" + data + "</data>"
    OtherServerSock.sendto(data.encode(), (server, SERVER_PORT))
    aidata, server = OtherServerSock.recvfrom(1024)
    return aidata.decode()

while True:
    data, addr = sock.recvfrom(1024)
    datadecode = data.decode()
    addr = str(addr)
    char1 = """('"""
    char2 = """',"""
    addr = str(addr[addr.find(char1)+2:addr.find(char2)])
    def LookForTags(datatosearch):
        if datatosearch in datadecode:
            return True
        else:
            return False
    if LookForTags("<data>") and LookForTags("</data>") and LookForTags("<key>") and LookForTags("</key>"):
        datatags = str(datadecode[datadecode.find("<data>")+6:datadecode.find("</data>")])
        keytags = str(datadecode[datadecode.find("<key>")+5:datadecode.find("</key>")])
        print("Data received from " + addr + """!
DATA: """ + datatags + """
KEY: """ + keytags)
        if len(keytags) >= 25:
            with open("keys.ini", "r") as keylist:
                keys = keylist.read()
                keylist.close()
            if keytags in keys:
                if datatags == "reload":
                    cw = [line.rstrip('\n') for line in open('controversialwords.ini')]
                    profanity.load_words(cw)
                    response = "Controversial word list reloaded!"
                elif profanity.contains_profanity(datatags) or NaziSymbol in datatags:
                    response = "ERROR: You cannot send controversial messages using this bot."
                elif 1 == 2:
                    response = LoadShifting("", datatags)
                else:
                    response = str(bot.get_response(datatags))
                    if profanity.contains_profanity(response):
                        response = str(profanity.censor(response))
                if addr == "127.0.0.1":
                    print("Please do not run applications that use the Slash API on the same machine as the server!")
                else:
                    sock.sendto(response.encode(), (addr, UDP_PORT))
            else:
                sock.sendto("INVALID KEY".encode(), (addr, UDP_PORT))
        else:
            print("Key invalid! Ignoring request!")
            sock.sendto("BAD KEY".encode(), (addr, UDP_PORT))
    else:
        print("Broken data received from " + addr + """!
DATA: """ + datadecode)
        sock.sendto("BAD DATA".encode(), (addr, UDP_PORT))
