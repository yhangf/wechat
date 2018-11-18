from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import itchat

app = Flask("wechat")
app.config.from_pyfile("settings.py")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from wechat import views, errors

app.add_template_global(itchat.search_chatrooms, "search_chatrooms")
app.add_template_global(itchat.update_chatroom, "update")
