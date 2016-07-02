# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app, socketio
from flask import request, render_template, Blueprint, url_for, redirect, session
import dbmongo, hashlib
from dbmongo import User, Data, Bid , Item
import subprocess, os
from subprocess import PIPE
from time import sleep
main = Blueprint('main', __name__)
# index page main route page

@main.route('/')
def index():
    item = Item.find()
    return render_template('shop.html',item = item)

@main.route('/buy/<itmid>', methods=['POST'])
def buyit(itmid):
    item = Item.finddata(itmid)
    many = request.form['many']
    if int(many) <= item.get('count'):
        return render_template('buy.html',**locals())
    else:
        return 'Fuck U NO GG'

@main.route('/keepbuy',methods=['POST'])
def keepbuy():
    item = request.form['item']
    many = request.form['many']
    combine = request.form['combine']
    print(combine)
    if int(many) <= Item.finddata(item).get('count') :
        if combine == "" :
            itm = {item:many}
            bid = Data.sent(itm)
            fitem = Data.find_item(bid)
            return render_template('result.html',**locals())
        else:
            if Data.find_item(combine) == None:
                itm = {item:many}
                bid = Data.sent(itm)
                fitem = Data.find_item(bid)
                return render_template('result.html',**locals())
            else:
                itm = Data.find_item(combine)
                if not itm.get(item) == None :
                    itmm = itm.get(item)
                    itm2 = {item:int(many)+int(itmm)}
                    itm.update(itm2)
                    bid = Data.update(combine,itm)                
                    fitem = Data.find_item(bid)
                    return render_template('result.html',**locals())
                else:
                    itm2 = {item:many}
                    itm.update(itm2)
                    bid = Data.update(combine,itm)                
                    fitem = Data.find_item(bid)
                    return render_template('result.html',**locals())


@main.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'GET':
        return render_template('find.html')
    else:
        bid = request.form['bid']
        stat = Data.find_bill(bid)
        if stat == False:
            fitem = Data.find_item(bid)
            return render_template('result.html',**locals())
        elif stat =='pre':
            return render_template('result/pre.html',bid = bid)
        elif stat =='nbid':
            dic = Bid.finddict(bid)
            u = Bid.findmoney(bid)
            return render_template('result/nbid.html',**locals())
        else:
            return render_template('warning.html',message = '單號並不存在!')

    
@app.route('/sent', methods=['GET', 'POST'])
def sent():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        urlp = request.form['url']
        texta = request.form['texta']
        if not name == "" and not mail == "" and not urlp == "" :
            return render_template('sent.html',**locals())
        else:
            return render_template('warning.html',message='請輸入完整資料謝謝！')


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        print('hi')
        name = request.form['name']
        mail = request.form['mail']
        urlp = request.form['url']
        texta = request.form['texta']
        ip_rmt = request.remote_addr
        bidinfo = dbmongo.Data.sent(name, mail, urlp, texta, ip_rmt)
        return render_template('save.html',bid = str(bidinfo))
    else:
        return render_template('index.html')



# init route to first time use
@app.route('/init', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        import hashlib
        hashsha = hashlib.sha256(passd.replace('\n', '').encode())
        # ManageSQL.addUser(user, hashsha.hexdigest(), '1', '0')
        User.add(user, hashsha.hexdigest(), '0','0', '1')

        return redirect(url_for('main.index'))
    else:
        return render_template('first.html')

# test of adduser route page 
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        user = request.form['buser']
        if LoginSQL.getPass(user) is None:
            import hashlib
            import random
            ans = random.uniform(1, 10)
            hashpass1 = hashlib.sha1(str(ans).encode())
            passd1 = hashpass1.hexdigest()
            hashpass0 = hashlib.sha256(passd1.replace('\n', '').encode())
            ManageSQL.addUser(user, hashpass0.hexdigest(), '0', '1')
            return passd1
        else:
            return '使用者已經他媽的存在了喔！'

