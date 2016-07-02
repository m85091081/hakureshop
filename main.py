#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muMDAU Server
from muMDAU_app import app , socketio
import sys, os, setting, logging
from muMDAU_app.index import main
from muMDAU_app.admin import admin
from muMDAU_app.bid import bid
from muMDAU_app.login import login
import muMDAU_app.logout 
from flask_socketio import SocketIO
from flask import Flask, render_template

app.secret_key =  setting.yourkey
app.register_blueprint(main)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(bid, url_prefix='/bid')
app.config['DEBUG'] = setting.debug


# Main function of MDAUServer
if __name__ == '__main__':
    socketio.run(app,host=setting.host,port=setting.port)

