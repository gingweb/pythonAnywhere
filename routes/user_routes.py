from flask import Blueprint, jsonify
from app import connect_to_mysql  # นำเข้าฟังก์ชัน connect_to_mysql จาก app.py

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    connection = connect_to_mysql()  # เรียกใช้ฟังก์ชัน connect_to_mysql ที่นำเข้ามา
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user"
            cursor.execute(sql)
            users = cursor.fetchall()
    finally:
        connection.close()

    return jsonify(users)
