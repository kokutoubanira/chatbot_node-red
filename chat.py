import os
from collections import deque
from flask import Flask, render_template, url_for
from flask_uwsgi_websocket import GeventWebSocket

app = Flask(__name__)
ws = GeventWebSocket(app)
users = {}
backlog = deque(maxlen=10)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def index():
    return render_template('index.html')


@ws.route('/websocket')
def chat(ws):
    users[ws.id] = ws

    for msg in backlog:
        ws.send(msg)

    while True:
        msg = ws.receive()
        if msg is None:
            break
        if msg == b"":
            continue

        backlog.append(msg)
        for id in users:
            if id != ws.id:
                users[id].send(msg)

    del users[ws.id]
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, gevent=100)