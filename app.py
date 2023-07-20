from flask import Flask
from user_routes import user_bp
from post_routes import post_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

if __name__ == '__main__':
    app.run()
