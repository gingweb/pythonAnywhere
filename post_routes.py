from flask import Blueprint, jsonify

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(message="รายการโพสต์ทั้งหมด")

@post_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    return jsonify(message=f"เนื้อหาโพสต์ ID {post_id}")
