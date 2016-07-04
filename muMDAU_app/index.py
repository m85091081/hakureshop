# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app, socketio
from flask import make_response, request, render_template, Blueprint, url_for, redirect, session
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
    if many == "" :
        many = int(1)
    if int(many) <= item.get('count'):
        return render_template('buy.html',**locals())
    else:
        return 'Fuck U NO GG'

@main.route('/delbidc')
def delbidc():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('bid','',expires=0)
    return response

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
            response = make_response(render_template('result.html',**locals()))
            response.set_cookie('bid',bid)
            return response
        else:
            if Data.find_item(combine) == None:
                itm = {item:many}
                bid = Data.sent(itm)
                fitem = Data.find_item(bid)
                response = make_response(render_template('result.html',**locals()))
                response.set_cookie('bid',bid)
                return response
            else:
                itm = Data.find_item(combine)
                if not itm.get(item) == None :
                    itmm = itm.get(item)
                    itm2 = {item:int(many)+int(itmm)}
                    itm.update(itm2)
                    bid = Data.update(combine,itm)                
                    fitem = Data.find_item(bid)
                    response = make_response(render_template('result.html',**locals()))
                    response.set_cookie('bid',bid)
                    return response
                else:
                    itm2 = {item:many}
                    itm.update(itm2)
                    bid = Data.update(combine,itm)                
                    fitem = Data.find_item(bid)
                    response = make_response(render_template('result.html',**locals()))
                    response.set_cookie('bid',bid)
                    return response


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

