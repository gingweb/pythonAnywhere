from flask import Blueprint, jsonify

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    # สำหรับตัวอย่างนี้จะให้เราเพียง return ข้อความเพื่อตอบกลับ
    return jsonify(message="รายชื่อผู้ใช้งานทั้งหมด")

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(message=f"ข้อมูลผู้ใช้งาน ID {user_id}")
