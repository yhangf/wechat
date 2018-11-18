import json
import time

import itchat
from itchat.content import *

from wechat import app, db
from wechat.forms import sendForm
from wechat.models import Message, Friends
from flask import flash, redirect, url_for, render_template, request, session


itchat.auto_login(hotReload=True)
# itchat.dump_login_status()

chatrooms = json.loads(
                    json.dumps(itchat.get_chatrooms(update=True), ensure_ascii=False)
                    )
memberList = json.loads(
                    json.dumps(itchat.get_friends(), ensure_ascii=False)
                    )

def save_friends(memberList):
    for member in memberList:
        try:
            friend = Friends(
                    NickName = member["NickName"],
                    RemarkName = member["RemarkName"],
                    Signature = member["Signature"]
                    )
            db.session.add(friend)
            db.session.commit()
        except:
            pass

@itchat.msg_register(TEXT, isGroupChat=True)
def group_reply_text(msg):

    chatroom_id = msg['FromUserName']

    username = msg['ActualNickName']

    if msg['Type'] == TEXT:
        content = msg['Content']
        message = Message(group_name=chatroom_id, name=username, text=content)
        db.session.add(message)
        db.session.commit()

@itchat.msg_register(TEXT)
def simple_reply(msg):
    return "[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的的信息：%s\n" % (msg['Text'])


@app.before_first_request
def init_db():
    # db.drop_all()
    # db.create_all()
    save_friends(memberList)

@app.route("/friends", methods=["GET", "POST"])
def get_friends():
    page = request.args.get("page", 1, type=int)
    pagination = Friends.query.order_by(Friends.id).paginate(
            page, per_page=8
            )
    friends = pagination.items
    return render_template("friends.html", pagination=pagination, friends=friends)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/replay', methods=["GET", "POST"])
def replay():
    return render_template("replay.html")

@app.route("/chatrooms", methods=["GET", "POST"])
def get_chatrooms():
    return render_template("chatrooms.html", chatrooms=chatrooms)

@app.route("/init", methods=["GET", "POST"])
def init():
    itchat.run()

@app.route("/spy", methods=["GET", "POST"])
def spy():
    page = request.args.get("page", 1, type=int)
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(
            page, per_page=5
    )
    messages = pagination.items
    return render_template("spy.html", pagination=pagination, messages=messages)

@app.route('/send', methods=["GET", "POST"])
def send():
    form = sendForm()
    if form.validate_on_submit():
        nickname = form.name.data
        message = form.message.data
        name = itchat.search_friends(name=nickname)
        username = name[0]["UserName"]
        itchat.send(message, username)
        flash('发送成功!')
        return redirect(url_for("send"))
    return render_template("send.html", form=form)
