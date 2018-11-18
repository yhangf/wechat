from datetime import datetime

from wechat import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50))
    name = db.Column(db.String(20))
    text = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Friends(db.Model):
    id = db.Column(db.Integer)
    NickName = db.Column(db.String(50), primary_key=True)
    RemarkName = db.Column(db.String(50))
    Signature = db.Column(db.String(50))
