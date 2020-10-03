#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

print("Welcome to Nathan's File-Transfer Lab!")

while True:
    try:
        fileName = input("Please enter the name of the file you'd like to send: ")
        file = open("./FilesToSend/" + fileName, "rb")
        break
    except FileNotFoundError:
        print("File does not exist, please enter another file name to try again")

paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

fileContents = file.read()

if len(fileContents) == 0:
    print("File is empty, exiting")
    sys.exit(1)

print("sending fileName")

framedSend(s, fileName, fileContents, debug)
