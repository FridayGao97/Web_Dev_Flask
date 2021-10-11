from flask import Flask

webapp = Flask(__name__,
            static_url_path='', 
            static_folder='templates',)


from app import main
from app import send_email
from app import home
