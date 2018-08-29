from app import db,login_manager,admin
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from flask import redirect,url_for

class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    email=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    head_img = db.Column(db.Unicode(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribut')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password) 

    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from jinja2 import Markup
from config import Config

class UserView(ModelView):
    column_labels = {
    'id':'编号',
    'username':'用户名',
    'email':'邮箱',
    'member_since':'注册时间',
    'last_seen':'最后一次登录时间',
    'head_img':'头像'
    }
    column_list =('id','username','email','member_since','last_seen','head_img')
    column_searchable_list = ['username', 'email']

    def _list_thumbnail(view, context, model, name):
        if not model.head_img:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                               filename=form.thumbgen_filename(model.head_img)))

    column_formatters = {
        'head_img': _list_thumbnail
    }

    form_extra_fields = {
        'head_img': form.ImageUploadField('头像',
                                     base_path=Config.UPLOADED_PATH,
                                     relative_path='head_img/',
                                     thumbnail_size=(60, 60, True))
    } 
    
    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))

from sqlalchemy.event import listens_for
import os
import os.path as op

@listens_for(User, 'after_delete')
def del_image(mapper, connection, target):
    if target.head_img:
        # Delete image
        try:
            os.remove(op.join(Config.UPLOADED_PATH, target.head_img))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(Config.UPLOADED_PATH,
                              form.thumbgen_filename(target.head_img)))
        except OSError:
            pass

