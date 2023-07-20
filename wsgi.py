import sys
import os

# เปลี่ยนเป็น path ที่เก็บ Flask app ของคุณ
path = '/home/ananya1989/mysite'
if path not in sys.path:
    sys.path.append(path)

# นำเข้า Flask app
# from flask_app import app as application
from app import app as application
