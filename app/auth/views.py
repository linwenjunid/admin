from flask_admin import BaseView, expose, AdminIndexView
from flask import flash,redirect,url_for
from flask_login import login_user,login_required,logout_user,current_user
from .forms import LoginForm
from ..models.user import User

class AuthView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))
        return self.render('index.html')

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                return self.render('index.html')
            flash('用户名或密码错误.')
        return self.render('auth/login.html',form=form)
    def __init__(self, **kwargs):
        super(AuthView, self).__init__(**kwargs)

class LogoutView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def login(self):
        logout_user()
        flash('你已退出登录。')
        return redirect(url_for('admin.index'))

    def is_accessible(self):
        return current_user.is_authenticated

