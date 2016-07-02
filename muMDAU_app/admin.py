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


@admin.route('/dbid/<bid>', methods=['GET', 'POST'])
def delbid(bid):
    if request.method == 'GET':
        return render_template("admin/del.html",bid = bid)

@admin.route('/check/<bid>')
def checka(bid):
    if 'otpusername' in session and 'username' in session:
        col = [{'name':'cpu','fname':'處裡器'},{'name':'mb','fname':'主機板'},{'name':'ram','fname':'記憶體'},{'name':'vga','fname':'顯示卡'},{'name':'disk','fname':'儲存裝置'},{'name':'psu','fname':'電源供應器'},{'name':'case','fname':'機殼'},{'name':'lcd','fname':'螢幕'},{'name':'soft','fname':'正版軟體'},{'name':'oth','fname':'其他'}]
        url = Data.find_one(bid,'url')
        name = Data.find_one(bid,'name')
        return render_template("admin/check.html",**locals())
    else:
        return redirect(url_for("admin.index"))

@admin.route('/check/save/<bid>', methods=['GET', 'POST'])
def checkdb(bid):
    if request.method=='POST':
        cpu= request.form.getlist('cpu[]')
        mb= request.form.getlist('mb[]')
        ram= request.form.getlist('ram[]')
        vga= request.form.getlist('vga[]')
        disk= request.form.getlist('disk[]')
        psu= request.form.getlist('psu[]')
        case= request.form.getlist('case[]')
        lcd= request.form.getlist('lcd[]')
        soft= request.form.getlist('soft[]')
        oth= request.form.getlist('oth[]')
        texta= request.form.get('texta')
        url = Data.find_one(bid,'url')
        name = Data.find_one(bid,'name')
        email = Data.find_one(bid,'email')
        dic = [{'fname':'處裡器','name':'cpu','value':cpu},{'fname':'主機板','name':'mb','value':mb },{'fname':'記憶體','name':'ram','value':ram},{'fname':'顯示卡','name':'vga','value':vga},{'fname':'存放裝置','name':'disk','value':disk},{'fname':'電源供應','name':'psu','value':psu},{'fname':'機殼','name':'case','value':case},{'fname':'螢幕','name':'lcd','value':lcd},{'fname':'軟體','name':'soft','value':soft},{'fname':'其他','name':'oth','value':oth}]
        u = 0
        for x in dic :
            if not '' in x.get('value'):
                for xx in range(len(x.get('value'))//3):
                    u = u + int(x.get('value')[xx *3 -1])
        print(u)
        Bid.presave(bid,u,name, email, url, texta, dic)
        Data.modshow(bid)
        Data.modstat(bid,'pre')
        return render_template("admin/cbid.html",**locals())

@admin.route('/check/publish/<bid>', methods=['GET', 'POST']) 
def pubbid(bid):
    if request.method=='GET':
        dic = Bid.finddict(bid)
        url = Data.find_one(bid,'url')
        u = 0
        name = Data.find_one(bid,'name')
        bid = bid
        for x in dic :
            if not '' in x.get('value'):
                for xx in range(len(x.get('value'))//3):
                    u = u + int(x.get('value')[xx *3 -1])
        return render_template("admin/publish.html",**locals())
    else:
        Data.modstat(bid,'nbid')
        return redirect(url_for('admin.index'))

@app.route('/save/db/<bid>', methods=['GET', 'POST'])
def savedb(bid):
    if request.method=='POST':
        return Bid.save(bid)
    
