#!/usr/bin/env python3

'''
The server program runs indifinitely (or until closed) waiting on users to connect. 
It waits for HTTP requests, and serves the client the relevant resource.
'''

__author__ = "Brian Bell"


import _thread as thread
import datetime
import re
from socket import *


SERVER_HOST = ''    # All available interfaces
SERVER_PORT = 5035  # My range is 5030-5039

OK_REQUEST = "200 OK"
BAD_REQUEST = "400 Bad Request"
NOT_FOUND = "404 Not Found"

sock_obj = socket(AF_INET, SOCK_STREAM)
sock_obj.bind((SERVER_HOST, SERVER_PORT))
sock_obj.listen(5)  # 5 pending connections before new ones rejected

def getReponse(data):
    '''
    Expects a string containing an HTTP request. Returns a response as a string.
    '''
    lines = data.split()
    print(lines)


    if len(lines) < 3 or lines[0] != "GET":
        return BAD_REQUEST
    
    try:
        response = ''
        with open(lines[1], 'r') as file:
            response =   OK_REQUEST
            for line in file:
                response  += line
        return response
    except FileNotFoundError:
        return NOT_FOUND
    
    

def handleClient(connection):
    '''
    Keeps connection open with client. Receives input and sends response as string of bytes. 
    '''
    while True:
        data = connection.recv(1024)
        if not data: break
        reply = getReponse(data.decode()) + "\r\n"
        connection.send(reply.encode())
    connection.close()

def listen():
    '''
    Listens on socket for clients to connect. Dispatches them to a new thread.
    '''
    client_num = 1
    while True:
        connection, addr = sock_obj.accept()
        print("Server connected to by Client %d at %s" % (client_num, addr))
        client_num += 1
        thread.start_new_thread(handleClient, (connection,))
        
        
listen()