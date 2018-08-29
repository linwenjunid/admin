from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_babelex import Babel

bootstrap=Bootstrap()
moment=Moment()
db=SQLAlchemy()
conf=Config()
admin=Admin(name='管理')
babel = Babel()

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
login_manager.login_message='请先登录。'

def create_app():
    app=Flask(__name__)
    app.config.from_object(conf)

    conf.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    from .auth.views import AuthView
    admin.init_app(app,index_view=AuthView(name='登录',url='/'),url='/')

    from .models.user import UserView
    admin.add_view(UserView(db.session,name='用户'))

    from .file.views import FileView
    admin.add_view(FileView())

    from .auth.views import LogoutView
    admin.add_view(LogoutView(name='退出'))

    return app
