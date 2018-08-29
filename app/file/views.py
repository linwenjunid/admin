from flask_admin.contrib.fileadmin import FileAdmin
from flask import flash,redirect,url_for,current_app
from flask_login import current_user
from config import Config

class FileView(FileAdmin):

    column_labels = {
    'name':'文件名',
    'size':'大小',
    'date':'日期',
    }

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))

    def is_accessible(self):
        return current_user.is_authenticated

    def __init__(self):
        import os.path as op
        import os
        path = op.join(Config.UPLOADED_PATH, 'files')
        try:
            os.mkdir(path)
        except OSError:
            pass

        #/static/files/静态资源路径要准确
        super(FileView, self).__init__(path,'/static/files/',name='文件')

