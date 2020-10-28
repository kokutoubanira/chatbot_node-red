import json
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chat")
def get_request():
    value = request.args.get('text', '')
    callback = request.args.get('callback', '')
    if (value.find('おはよう') != -1):
        value = 'おはようございます。<br>ごきげんはいかがですか？'
    if (value.find('元気') != -1):
        value = '元気でよかったですね'
    if (value.find('天気') != -1):
        value = '今日の天気は晴れです。'
    dic = {'output' : [{'type' : 'text', 'value' : value }] }
    contents = callback + '(' + json.dumps(dic) + ')'
    return contents


if __name__ == "__main__":
    app.run(host="0.0.0.0")