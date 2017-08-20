from flask_script import Manager
from api.api import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT0", 5000))
    app.run(host='0.0.0.0',port=port)