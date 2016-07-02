# -*- coding: utf-8 -*-
from muMDAU_app import app
from flask import session, redirect, url_for

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('otpusername', None)
    return redirect(url_for('main.index'))
