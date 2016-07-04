# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app, socketio , login
from threading import Thread
from flask import request, render_template, Blueprint, url_for, redirect, session
from dbmongo import User,Data,Bid,Item
import subprocess, os
from subprocess import PIPE
from time import sleep
admin = Blueprint('admin', __name__)
thread = None
# index page main route page 
@admin.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'otpusername' in session and 'username' in session:
            data = Bid.bidfind()
            return render_template('admin/adm.html',**locals())
        elif 'otpusername' not in session and 'username'  in session:
            return redirect(url_for("login.ologin"))
        else:
            return render_template("admin/login.html")
    else:
        name = request.form['name']
        artist = request.form['artist']
        des = request.form['des']
        count = int(request.form['count'])
        tag = request.form['tag']
        cost = request.form['cost']
        pic = request.form['pic']
        if not name == "" and not artist == "" and not des == "" and not count == "" and not tag == "" and not pic == "" and not cost == "":
            Item.new(name,artist,des,count,tag,cost,pic)
            return redirect(url_for("main.index"))

