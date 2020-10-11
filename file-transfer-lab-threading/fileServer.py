#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


while True:
    sock, addr = lsock.accept()

    if not os.fork():
        print("connection rec'd from", addr)
        # sys.exit(1)

        payload = ""
        try:
            fileName, fileContents = framedReceive(sock, debug)
        except:
            print("File transfer failed")
            sys.exit(1)

        if debug: print("rec'd: ", payload)

        if payload is None:
            print("File contents were empty, exiting...")
            sys.exit(1)

        fileName = fileName.decode()

        try:
            if not os.path.isfile("./ReceivedFiles/" + fileName):
                file = open("./ReceivedFiles/" + fileName, 'w+b')
                # print("FC:", fileContents)
                file.write(fileContents)
                file.close()
                print("File", fileName, "successfully accepted!")
                sys.exit(0)
            else:
                print("File with name", fileName, "already exists on server. exiting...")
                sys.exit(1)
        except FileNotFoundError:
            print("Fail")
            sys.exit(1)
