from flask import Flask
import secrets
from endpoints import blueprint as api_v1


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.url_map.strict_slashes = False

app.register_blueprint(api_v1)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
