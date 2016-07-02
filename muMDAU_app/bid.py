from muMDAU_app import app, socketio, csrf
from muMDAU_app.pyallpay import AllPay
from flask import request, render_template, Blueprint
from dbmongo import User, Data, Bid ,Item
import datetime
bid = Blueprint('bid', __name__)

@csrf.exempt
@bid.route('/server/csrf', methods=['GET','POST'])
def server():
    ip = request.headers.get('X-Real-Ip', request.remote_addr)
    if request.method == 'POST':
        if ip == '60.199.179.34' or ip == '60.199.179.35'  or ip == '60.199.179.36' or ip == '60.199.179.37' or ip == '60.199.179.38' or ip == '60.199.179.53' or ip == '175.99.72.125':
            MerchantTradeNo = request.form['MerchantTradeNo']
            RtnCode = request.form['RtnCode']
            SimulatePaid = request.form['SimulatePaid']
            if not int(SimulatePaid) == 1 :
                if int(request.form['TradeAmt']) == int(Bid.findmoney( str(MerchantTradeNo[0:16]))):
                    Data.modbill(str(MerchantTradeNo[0:16]))
                    Bid.modbill(str(MerchantTradeNo[0:16]))
                return '1|OK'
            else:
                print('simi!')
                return '1|OK'
        return '0|no allpay'

@csrf.exempt
@bid.route('/result',methods=['POST'])
def resallfuck():
    response = make_response(render_template('orderresult.html'))
    response.set_cookie('bid','',expires=0)
    return response

@bid.route('/gen/full/<bid>',methods=['POST'])
def allfuck(bid):
    name = request.form['name']
    tele = request.form['tele']
    email = request.form['email']
    addr = request.form['address']
    if name == "" and tele == "" and email =="" and addr=="":
        return "fuck u gg"
    else:
        merchant_trade_no = bid + str(Data.find_one(bid,'genabid'))
        fitem = Data.find_item(bid)
        money = 80
        for f in fitem :
            money = money + int(Item.finddata(f).get('cost')) * int(fitem[f])
        Data.modgenabid(bid)
        payment_info = {'TotalAmount': int(money), 'ChoosePayment': 'ALL', 'MerchantTradeNo': merchant_trade_no, 'ItemName': "test"}
        ap = AllPay(payment_info)
        dict_url = ap.check_out()
        genpay = ap.gen_check_out_form(dict_url)
        Bid.bidadd(bid, money , name ,email ,addr ,tele)
        return render_template('allpay.html',genpay = genpay)
