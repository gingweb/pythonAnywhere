from flask import Flask
import pymysql

app = Flask(__name__)

# กำหนดข้อมูลการเชื่อมต่อ MySQL
db_config = {
    'host': 'ananya1989.mysql.pythonanywhere-services.com',
    'user': 'ananya1989',
    'password': 'gingZAB28',
    'db': 'ananya1989$default',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# สร้างฟังก์ชันเพื่อเชื่อมต่อกับ MySQL
def connect_to_mysql():
    connection = pymysql.connect(**db_config)
    return connection

# Register Blueprint
from user_routes import user_bp
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run()
