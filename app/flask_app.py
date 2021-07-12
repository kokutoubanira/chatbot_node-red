from flask import Flask, jsonify, request
from gensim.models import word2vec
import json
import MeCab

import requests
import json
from datetime import datetime, timedelta, time
import sqlite3
import sqlite3

app = Flask(__name__)

prefs = ["北海道","青森","岩手","宮城","秋田","山形",
"福島","茨城","栃木","群馬","埼玉","千葉","東京","神奈川","新潟",
"富山","石川","福井","山梨","長野","岐阜","静岡","愛知","三重","滋賀",
"京都","大阪","兵庫","奈良","和歌山","鳥取","島根","岡山","広島","山口","徳島",
"香川","愛媛","高知","福岡","佐賀","長崎","熊本","大分","宮崎","鹿児島","沖縄"]
# wakati = MeCab.Tagger("-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
# words = wakati.parse("ここではきものを脱いでください").split()
# print(words)
# テキストから都道府県名が見つからない場合は空文字を返す

# 都道府県名から緯度と経度を取得するための辞書
latlondic = {'北海道': (43.06, 141.35), '青森': (40.82, 140.74), '岩手': (39.7, 141.15), '宮城': (38.27, 140.87),
                '秋田': (39.72, 140.1), '山形': (38.24, 140.36), '福島': (37.75, 140.47), '茨城': (36.34, 140.45),
                '栃木': (36.57, 139.88), '群馬': (36.39, 139.06), '埼玉': (35.86, 139.65), '千葉': (35.61, 140.12),
                '東京': (35.69, 139.69), '神奈川': (35.45, 139.64), '新潟': (37.9, 139.02), '富山': (36.7, 137.21),
                '石川': (36.59, 136.63), '福井': (36.07, 136.22), '山梨': (35.66, 138.57), '長野': (36.65, 138.18),
                '岐阜': (35.39, 136.72), '静岡': (34.98, 138.38), '愛知': (35.18, 136.91), '三重': (34.73, 136.51),
                '滋賀': (35.0, 135.87), '京都': (35.02, 135.76), '大阪': (34.69, 135.52), '兵庫': (34.69, 135.18),
                '奈良': (34.69, 135.83), '和歌山': (34.23, 135.17), '鳥取': (35.5, 134.24), '島根': (35.47, 133.05),
                '岡山': (34.66, 133.93), '広島': (34.4, 132.46), '山口': (34.19, 131.47), '徳島': (34.07, 134.56),
                '香川': (34.34, 134.04), '愛媛': (33.84, 132.77), '高知': (33.56, 133.53), '福岡': (33.61, 130.42),
                '佐賀': (33.25, 130.3), '長崎': (32.74, 129.87), '熊本': (32.79, 130.74), '大分': (33.24, 131.61),
                '宮崎': (31.91, 131.42), '鹿児島': (31.56, 130.56), '沖縄': (26.21, 127.68)}

current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
appid = 'c92cd5cc8e296e57239e20d8e3148479' # 自身のAPPIDを入れてください  

def get_current_weather(lat,lon):
# 天気情報を取得    
    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(current_weather_url,lat,lon,appid))
    return response.json()

def get_tomorrow_weather(lat, lon):
    #　今日の時間を取得
    today = datetime.today()
    # 明日の時間を取得
    tomorrow = today + timedelta(days=1)
    # 明日の正午の時間を取得
    tomorrow_noon = datetime.combine(tomorrow, time(12, 0))
    # UNIX時間に変換
    timestamp = tomorrow_noon.timestamp()
    #天気の
    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(forecast_url,lat,lon,appid))
    dic = response.json()
    #3時間おきの天気情報についてループ
    for i in range(len(dic["list"])):
        # i番目の天気情報(UNIX時間)
        dt = float(dic["list"][i]["dt"])
        # 明日の正午以降のデータになった時点でその天気情報を返す
        if dt >= timestamp:
            return dic["list"][i]
    return ""

cw = get_current_weather(43.06, 141.35)
print(cw["weather"][0]["description"])

tw = get_tomorrow_weather(43.06, 141.35)
print(tw["main"]["temp"])


cw = get_current_weather(43.06, 141.35)
print(cw["main"]["temp"])

tw = get_tomorrow_weather(43.06, 141.35)
print(tw["weather"][0]["description"])

def get_place(text):
    for pref in text:
        if pref in prefs:
            return pref
    return ""
# テキストに「今日」もしくは「明日」があればそれを返す．見つからない場合は空文字を返す．
def get_date(text):
    for i in text:
        if i in ["今日", "明日"]:
            return i
    return ""

wakati = MeCab.Tagger("-Owakati ")

@app.route('/weather_place', methods=["GET", 'POST'])
def weather_place():
    value = request.args.get('text', '')
    app.logger.debug(value)
    wakati_text = wakati.parse(value).split()
  
    app.logger.debug(wakati_text)
    text = get_place(wakati_text)
    
    return text

@app.route('/weather_date', methods=["GET", 'POST'])
def weather_date():
    value = request.args.get('text', '')
    app.logger.debug(value)
    wakati_text = wakati.parse(value).split()
    
    text = get_date(wakati_text)
    app.logger.debug(text)
    return text


@app.route('/get_weather', methods=["GET", 'POST'])
def get_weather():
    place = request.args.get('place', '')
    date = request.args.get('date', '')
    info = request.args.get('info', '')
    app.logger.debug([place, date, info])
    lat = latlondic[place][0]
    lon = latlondic[place][1]
    app.logger.debug(latlondic[place])
    if date == "今日":
        gw = get_current_weather(lat, lon)
    else :
        gw = get_tomorrow_weather(lat, lon)
    app.logger.debug(gw)
    if info != "気温":
        re = gw["weather"][0]["description"]
    else :
        re = str(gw["main"]["temp"]) + "度"
    app.logger.debug(re)
    return re

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)