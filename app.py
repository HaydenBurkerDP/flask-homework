from flask import Flask
from routes.user_routes import user

app = Flask(__name__)

app.register_blueprint(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8086", debug=True)
