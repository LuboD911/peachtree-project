from flask import Flask
from flask_jwt_extended import JWTManager
from config import SECRET_KEY
from transactions import transactions_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

app.register_blueprint(transactions_bp, url_prefix='/transactions')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
