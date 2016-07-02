# -*- coding: utf-8 -*-
# muMDAU_app init file 
# some debug code of server like update/restart code

from flask import Flask , render_template
from flask_socketio import SocketIO
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
csrf = CsrfProtect(app)
socketio = SocketIO(app)

