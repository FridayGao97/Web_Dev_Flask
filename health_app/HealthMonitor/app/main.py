from flask import render_template, url_for
from app import webapp
import sys
import threading
import time
from app.home import backgroundProcess
import multiprocessing 

global all_thread

@webapp.route('/')
def main():
    global all_thread 
    all_thread = []
    #create one bakcground thread
    for thread in threading.enumerate():
        all_thread.append(thread.name)

    
    if 'back-ground' not in all_thread:
        thread = threading.Thread(name='back-ground',target=backgroundProcess, args=())
        thread.daemon = True
        thread.start()


    return render_template("login.html")