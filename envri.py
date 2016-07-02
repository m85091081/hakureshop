#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muWatchdog runtime environment
import setting
import sys
import os
import socket
import subprocess
import socketio

# run master branch git pull to update server
def serverupdate():
    print('# Git status')
    subprocess.call(['git pull'], shell=True)

def rundebugapp():
    subprocess.call(['pypy3 '+setting.runpy+'.py'], shell=True)
   
    
# use subprocess to call MDAUServer
def runapp():
    subprocess.call(['gunicorn -b '+ str(setting.host) +':'+ str(setting.port) + ' ' +setting.runpy+':'+ setting.entry], shell=True)

# use socket to check port open
def portcheck(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        return s.connect_ex(('localhost', port)) != 0
    finally:
        s.close()

# Main class 
if __name__ == '__main__':
    # loop for all time
    while 1:
        if setting.debug is True :
            if portcheck(setting.port):
                rundebugapp()
        else:
            print('Now 0mu-WatchDog is run')
            if portcheck(setting.port):
                runapp()
