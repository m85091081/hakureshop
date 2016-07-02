# -*- coding: utf-8 -*-

from muMDAU_app import app 
from flask import Blueprint, session, redirect, url_for, request, render_template
import hashlib
from dbmongo import User
login = Blueprint('login', __name__)
@login.route('', methods=['GET', 'POST'])
def dologin():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']

        password = User.login(user)

        if not password:
            return '帳號錯誤'
        else:
            hashsha = hashlib.sha256(passd.replace('\n', '').encode())
            if password == hashsha.hexdigest():
                session['username'] = user
                session['admgrp'] = User.findgrp(str(user))
                return redirect(url_for('login.ologin'))
            else:
                return '密碼錯誤'

    else:
        return redirect(url_for('admin.login'))

@login.route('/otp', methods=['GET', 'POST'])
def ologin():
    if request.method == 'GET':
        if 'otpusername' not in session and 'username'in session :
            if User.otpchk(str(session['username'])) == "0":
                print("hellop")
                import pyotp
                key = pyotp.random_base32()
                totp = pyotp.TOTP(key)
                optsct = totp.provisioning_uri(session['username'])
                User.optnew(str(session['username']),optsct,key)
                return render_template('admin/otpset.html',otpurl=str(User.otpchk(str(session['username']))))
            else:
                return render_template('admin/otplogin.html',name=str(session['username']))
        else:
            return redirect(url_for('admin.index'))

    else:
        if 'username' in session:
            import pyotp
            passd = request.form['otppass']
            otpkey = User.otpkeychk(str(session['username']))
            totp = pyotp.TOTP(otpkey)
            if totp.verify(passd) is True:
                session['otpusername'] = str(session['username'])+str(passd)
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('login.ologin'))

