from flask_script import Manager
from api import api
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT0", 5000))
    api.app.run(host='0.0.0.0',port=port)
# manager.run()