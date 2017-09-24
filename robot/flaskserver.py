'''
Created on 23 Sep 2017

@author: pi
'''
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('index2.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
