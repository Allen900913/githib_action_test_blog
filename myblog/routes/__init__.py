from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PWD  = os.getenv("MYSQL_PWD", "123456")
MYSQL_DB   = os.getenv("MYSQL_DB", "myblog_db")


app = Flask(__name__ , 
            template_folder='../templates', 
            static_folder='../assets', 
            static_url_path='/assets'
            )

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# 導入路由模組（必須在 app 創建後）
from . import user_routes, admin_routes
