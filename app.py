#coding: utf-8

from flask import Flask, request, render_template
import requests
import json

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    users = {}
    with open("users.json", "r", encoding="utf-8") as f:
        data = f.read()
        users = json.loads(data)

    return render_template("home.html", users=users)

@app.route("/api/check_id", methods=["POST"])
def check_id():
    username = request.form["username"]
    users = {}
    with open("users.json", "r", encoding="utf-8") as f:
        data = f.read()
        users = json.loads(data)

    for user in users:
        if username == user["username"]:
            return user["userid"]

    return "Error"

@app.route("/api/check_coupon", methods=["POST"])
def check_coupon():
    userid = request.form["userid"]
    coupon = request.form["coupon"]
    
    data = {
        # "npaCode": "07901CQ10406Q",
        # "couponNum": "LUPU2VAVWN",
        "npaCode": userid,
        "couponNum": coupon,
        "region": "KR"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "Cookie": "PCID=16357799776188379794221; _hjid=388a4ac5-d5c5-4786-b50c-186ca50fe7a7; _ga_GWPD7HDK9M=GS1.1.1636541618.3.0.1636541618.0; _hjSessionUser_1327448=eyJpZCI6ImQyODBmM2Q1LTA1NDctNWIyNS04NmY0LWJmNjk1YTdmMmI1ZSIsImNyZWF0ZWQiOjE2NDA3ODMxNTU0MzYsImV4aXN0aW5nIjp0cnVlfQ==; _ga_YVXQ064DKG=GS1.1.1647848642.1.1.1647848657.0; _ga_HN5G885YR0=GS1.1.1648661345.1.1.1648661379.0; _gcl_au=1.1.431093251.1650895379; A2SK=act:16508953894741024103; NXTPA=-; NXGID=A52EFC5DCE0C0B06702254975E0B4ABF; PS_NexonID=4UIl8SD5INus8zbw6iJKlGDyqKSc9flnNPOsOG1pzM4%253d; NXABP=; GGAN=0; NXMP=; _gid=GA1.2.1191055630.1652186280; JSESSIONID=FB3F4D3DFE96BFFECD5A046F6874AE16; isCafe=false; _ga_NEHB476HQQ=GS1.1.1652472456.5.1.1652472460.0; _hjSession_1327448=eyJpZCI6IjhkNDg5YzMzLWFjZGMtNDI3MS05NzI5LThiOTE3ZTk0YTdhYiIsImNyZWF0ZWQiOjE2NTI0NzkwMTMwMjIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; IL=; NXCH=; IM=0; RDB=; NPP=; ENC=; NXLW=SID=0DDB8056192AD20D2F9ADCC48B593E4F&PTC=https:&DOM=kartrideresports.nexon.com&ID=&CP=; _ga=GA1.2.1575722911.1635779978; _ga_3Q73DZJDDP=GS1.1.1652479902.37.0.1652479902.0; _ga_D78NYXY4CE=GS1.1.1652479012.7.1.1652479903.0"
    }
    r = requests.post("https://mcoupon.nexon.com/kartrush/findUserNpa", headers=headers, json=data, verify=False)
    # code 2200 : ?????? ????????? ?????? ?????????. ?????? ?????? ??? ?????? ??????????????????.
    # code 1101 : ????????? ???????????? ?????????. ?????? ?????? ??? ?????? ??????????????????
    # https://mcoupon.nexon.com/kartrush/findUserNpa
    # {"result":true,"info":[{"id":"16520000001680394","name":"???????????????"}]}
    
    print(r.text)

    if "\"code\":2200" in r.text:
        return "{\"result\":\"false\", \"message\":\"?????? ????????? ?????? ?????????.\"}"
    elif "\"code\":1101" in r.text:
        return "{\"result\":\"false\", \"message\":\"????????? ???????????? ?????????.\"}"
    elif "\"code\":91001" in r.text:
        return "{\"result\":\"false\", \"message\":\"?????? ????????? ????????? ??????????????????.\"}"
    elif "\"code\":91002" in r.text:
        return "{\"result\":\"false\", \"message\":\"?????? ????????? ????????? ??????????????????.\"}"
    elif "\"result\":true" in r.text:
        return r.text
    else:
        return "{\"result\":\"false\", \"message\":\"?????? ?????? ??????\"}"

@app.route("/api/submit_coupon", methods=["POST"])
def submit_coupon():
    # https://mcoupon.nexon.com/kartrush/useGiftCoupon
    # {"npaCode":"07901CQ10406Q","couponNum":"LUPU2VAVWN","id":"16520000001680394","name":"???????????????","region":"KR"}
    userid = request.form["userid"]
    coupon = request.form["coupon"]
    account_id = request.form["account_id"]
    account_name = request.form["account_name"]
    data = {
        # "npaCode": "07901CQ10406Q",
        # "couponNum": "LUPU2VAVWN",
        "npaCode": userid,
        "couponNum": coupon,
        "id": account_id,
        "name": account_name,
        "region": "KR"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "Cookie": "PCID=16357799776188379794221; _hjid=388a4ac5-d5c5-4786-b50c-186ca50fe7a7; _ga_GWPD7HDK9M=GS1.1.1636541618.3.0.1636541618.0; _hjSessionUser_1327448=eyJpZCI6ImQyODBmM2Q1LTA1NDctNWIyNS04NmY0LWJmNjk1YTdmMmI1ZSIsImNyZWF0ZWQiOjE2NDA3ODMxNTU0MzYsImV4aXN0aW5nIjp0cnVlfQ==; _ga_YVXQ064DKG=GS1.1.1647848642.1.1.1647848657.0; _ga_HN5G885YR0=GS1.1.1648661345.1.1.1648661379.0; _gcl_au=1.1.431093251.1650895379; A2SK=act:16508953894741024103; NXTPA=-; NXGID=A52EFC5DCE0C0B06702254975E0B4ABF; PS_NexonID=4UIl8SD5INus8zbw6iJKlGDyqKSc9flnNPOsOG1pzM4%253d; NXABP=; GGAN=0; NXMP=; _gid=GA1.2.1191055630.1652186280; JSESSIONID=FB3F4D3DFE96BFFECD5A046F6874AE16; isCafe=false; _ga_NEHB476HQQ=GS1.1.1652472456.5.1.1652472460.0; _hjSession_1327448=eyJpZCI6IjhkNDg5YzMzLWFjZGMtNDI3MS05NzI5LThiOTE3ZTk0YTdhYiIsImNyZWF0ZWQiOjE2NTI0NzkwMTMwMjIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; IL=; NXCH=; IM=0; RDB=; NPP=; ENC=; NXLW=SID=0DDB8056192AD20D2F9ADCC48B593E4F&PTC=https:&DOM=kartrideresports.nexon.com&ID=&CP=; _ga=GA1.2.1575722911.1635779978; _ga_3Q73DZJDDP=GS1.1.1652479902.37.0.1652479902.0; _ga_D78NYXY4CE=GS1.1.1652479012.7.1.1652479903.0"
    }

    r = requests.post("https://mcoupon.nexon.com/kartrush/useGiftCoupon", headers=headers, json=data, verify=False)
    print(r.text)

    return "1"

@app.route("/api/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    userid = request.form["userid"]
    password = request.form["password"]
    if password != "2468":
        return "??????????????? ???????????? ????????????."
    
    users = []
    with open("users.json", "r", encoding="utf-8") as f:
        data = f.read()
        users = json.loads(data)
        users.append({"username": username, "userid": userid})
    
    with open("users.json", "w", encoding="utf-8") as f:
        data = json.dumps(users, ensure_ascii=False)
        f.write(data)
    
    return "?????? ????????? ?????????????????????."

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8877)