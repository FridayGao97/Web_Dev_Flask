from flask import Flask

#webapp = Flask(__name__)
webapp = Flask(__name__,
            static_url_path='', 
            static_folder='templates',)


from app import log_in
from app import home
from app import main
from app import send_email
from app import register
from app import bodyConfig
from app import change_psw
# from app import create_ami
