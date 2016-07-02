import datetime
import setting 
from bson.objectid import ObjectId
from pymongo import MongoClient
from github import Github
from muMDAU_app import app
client = MongoClient(setting.mongohost)
db = client['HakureiShop']
import hashlib
class bidGen:
    def gen():
        num  = hashlib.sha384(str(datetime.datetime.now()).encode('utf8')).hexdigest().lower()
        num = num[2:8]
        num = datetime.datetime.now().strftime("%y%m%d%H%M") + num
        return str(num)

class InitDB:
    user = db['Users']


class Item:
    def new(name,artist,des,count,tag, cost,img):
        data = db['Item']
        data.create_index("name", unique=True)
        rsent = {
                "name" : name ,
                "artist" : artist ,
                "des" : des,
                "count" : count,
                "tag" : tag,
                "cost" : cost,
                "img" : img
                }
        data.insert_one(rsent)
        return 0
    def find():
        data = db['Item']
        dfind = data.find()
        return dfind
    def finddata(itmid):
        data = db['Item']
        dfind = data.find_one({"_id":ObjectId(itmid)})
        return dfind


class Data:
    def sent(itm):
        data = db['buyData']
        data.create_index("bid", unique=True)
        bid = bidGen.gen()
        rsent = { 
                "bid": bid ,
                "date": datetime.datetime.now(),
                "item" : itm,
                "genabid" : 0,
                "show" : True,
                "bill" : False
                }
        data.update_one({"bid":bid},{"$set": rsent} ,upsert=True)
        return bid
    
    def find_item(bid):
        data = db['buyData']
        dfind = data.find_one({"bid":str(bid)})
        try:
            durl = dfind.get('item') 
        except Exception as e:
            durl = None
        return durl
    
    def find_bill(bid):
        data = db['buyData']
        dfind = data.find_one({"bid":str(bid)})
        try:
            durl = dfind.get('bill') 
        except Exception as e:
            durl = None
        return durl
    def update(bid,item):
        data = db['buyData']
        rsent = { 
                "bid": bid ,
                "date": datetime.datetime.now(),
                "item" : item,
                "genabid": int(Data.find_one(bid,"genabid")),
                "show" : True,
                "bill" : False
                }
        data.update_one({"bid":bid},{"$set": rsent} ,upsert=True)
        return bid

    def find():
        data = db['Data']
        dfind = data.find()
        return dfind
    def find_one(bid,something):
        data = db['buyData']
        dfind = data.find_one({"bid":str(bid)})
        try:
            durl = dfind.get(str(something))
        except Exception as e:
            durl = None
        return durl
    def delete(bid):
        data = db['Data']
        dfind = data.delete_one({"bid":str(bid)})
        return 0
    def modshow(bid):
        data = db['Data']
        data.update_one({"bid": str(bid)},{"$set": {"show": False}})
        return 0
    def modgenabid(bid):
        data = db['buyData']
        data.update_one({"bid": str(bid)},{"$set": {"genabid": Data.find_one(bid,'genabid') + 1}})
        return 0
    def modstat(bid,stat):
        data = db['Data']
        data.update_one({"bid": str(bid)},{"$set": {"status": str(stat)}})
        return 0

class Bid:
    def bidadd(bid, bidmoney , name ,email ,addr ,tele):
        data = db['bidData']
        data.create_index("bid", unique=True)
        rsent = { 
                "bid": bid,
                "bill": bidmoney,
                "date": datetime.datetime.utcnow(),
                "name": name,
                "email": email,
                "addr" : addr,
                "tele" : tele,
                "bidornot" : False
                }
        rid = data.update_one({"bid":bid},{"$set": rsent} ,upsert=True).upserted_id
        return bid

    def prefind():
        data = db['preData']
        dfind = data.find()
        return dfind
    
    def bidfind():
        data = db['bidData']
        dfind = data.find()
        return dfind

    def presave(bid, bidmoney, name, email, url, texta, dic):
        data = db['preData']
        data.create_index("bid", unique=True)
        rsent = { 
                "bid": bid,
                "bidmoney": bidmoney,
                "date": datetime.datetime.utcnow(),
                "name": name,
                "email": email,
                "url" : url,
                "texta" : texta,
                "dic" : dic
                }

        rid = data.update_one({"bid":bid},{"$set": rsent} ,upsert=True).upserted_id
        return bid
    
    def finddict(bid):
        data = db['preData']
        dfind = data.find_one({"bid":bid})
        durl = dfind.get('dic')
        return durl

    def findmoney(bid):
        data = db['preData']
        dfind = data.find_one({"bid":bid})
        durl = dfind.get('bidmoney')
        return durl
    


    
class User:
    def add(username, password, otpky, otp, admin):
        user = db['Users']
        user.create_index("user", unique=True)
        raw = {"user": username,
                "password": password,
                "otpkey": otpky,
                "otp": otp,
                "admin": admin,
                "date": datetime.datetime.utcnow()}
        print(user.insert_one(raw).inserted_id)
    # group - 1-root 2-adm 3-out 4-in
    def findgrp(username):
        user = db['Users']
        usern = user.find_one({"user": username}) 
        group = usern['admin']
        return group

    def login(username):
        try:
            user = db['Users']
            usern = user.find_one({"user": username})
            password = usern['password'] 
        except:
            password = False
        return password
    def otpchk(username):
        user = db['Users']
        usern = user.find_one({"user": username}) 
        otp = usern['otp']
        return otp 
    def otpkeychk(username):
        user = db['Users']
        usern = user.find_one({"user": username}) 
        otp = usern['otpkey']
        return otp 
    def optnew(username,pyotp, otpky):
        user = db['Users']   
        user.update_one({"user": str(username)},{"$set": {"otp": str(pyotp)}})
        user.update_one({"user": str(username)},{"$set": {"otpkey": otpky}})

app.jinja_env.globals.update(getdata=Data.find_one)
app.jinja_env.globals.update(itemdata=Item.finddata)
