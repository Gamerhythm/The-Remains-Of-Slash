import socket

SLASH_UDP_HOSTNAME = "slashapi.tk"
SLASH_UDP_PORT = 6754
SLASH_UDP_IP = socket.gethostbyname(SLASH_UDP_HOSTNAME)
def reply(datatosend):
    global SLASH_UDP_PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", SLASH_UDP_PORT))
    with open("slashkey.ini", "r+") as keyfile:
        key = keyfile.read()
    datatosend = datatosend.lstrip(' ')
    datatosend = "<key>" + key + "</key>/n<data>" + datatosend + "</data>"
    sock.sendto(datatosend.encode(), (SLASH_UDP_IP, SLASH_UDP_PORT))
    slashdata, server = sock.recvfrom(1024)
    recieveddata = slashdata.decode()
    if recieveddata == "BAD KEY":
        recieveddata = "Slash had an issue resolving your API key. Please confirm it is correct and if you don't have one check the Slash website to find out how to get one."
    return recieveddata

if __name__ == '__main__':
    print("Slash API demo for Python. Created by Jake Gealer.")
    while True:
        text = input("> ")
        info = reply(text)
        print(info)
