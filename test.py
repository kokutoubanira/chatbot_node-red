from flask import Flask, jsonify, request
from gensim.models import word2vec
import json
import MeCab

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

def get_place(text):
    for pref in text:
        if pref in prefs:
            return pref
    return ""


wakati = MeCab.Tagger("-Owakati ")

@app.route('/weather_place', methods=["GET", 'POST'])
def weather_place():
    value = request.args.get('text', '')
    wakati_text = wakati.parse(value).split()
    with open("./wakati.txt", "w") as f:
        f.write(wakati.parse(value))
    
    print(wakati_text)
    text = get_place(wakati_text)
    
    return text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)