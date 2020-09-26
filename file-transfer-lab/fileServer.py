#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
sys.path.append("../framed-echo")
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

sock, addr = lsock.accept()

print("connection rec'd from", addr)

print("Receiving file name")
payload = ""

payload = framedReceive(sock, debug)
if debug: print("rec'd: ", payload)
# print(payload)
# payload += b"!"             # make emphatic!
# framedSend(sock, b'File received!', debug)

payload = payload.decode()

fileName = payload.split("$$%")[0]
fileContents = payload.split("$$%")[1]


try:
    if not os.path.isfile("./ReceivedFiles/" + fileName):
        file = open("./ReceivedFiles/" + fileName, 'w')
        file.write(fileContents)
        file.close()
except FileNotFoundError:
    print("Fail")

# try:
#     if os.path.isfile("./ReceivedFiles/" + payload.decode()):
#         file = open(payload.decode(), 'w')
#         print("Receiving file contents:")
#         while True:
#             payload = framedReceive(sock, debug)
#             if debug: print("rec'd: ", payload)
#             if not payload:
#                 break
#
#             print(payload.decode())
#             # payload += b"!"             # make emphatic!
#             framedSend(sock, payload, debug)
#
#         file.write(payload.decode())
# except FileNotFoundError:
#     print("I don't know when this would happen")

# print("Receiving file contents:")
# while True:
#     payload = framedReceive(sock, debug)
#     if debug: print("rec'd: ", payload)
#     if not payload:
#         break
#
#     print(payload.decode())
#     # payload += b"!"             # make emphatic!
#     framedSend(sock, payload, debug)
#
# file.write(payload.decode())