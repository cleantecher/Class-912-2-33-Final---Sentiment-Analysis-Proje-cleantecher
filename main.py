from flask import Flask, jsonify, render_template, request
from tweet import get_tweets, polarity
from replit import db


app = Flask(__name__)


@app.route('/')
def index():
    keyword = request.args.get('keyword')
    if keyword:
        my_tweets = get_tweets(keyword)
        sentiments = polarity(my_tweets, keyword)
    else:
        my_tweets = []
        sentiments = {}

    return render_template('index.html', tweets=my_tweets,
        sentiments=sentiments)


@app.route('/csvdata')
def data():
    return 'This will contain a csv data feed'


@app.route('/twitter/<keyword>')
def tweet_data(keyword):
    my_tweets = get_tweets(keyword)
    sentiments = polarity(my_tweets, keyword)
    data = db[keyword]
    print(data)
    return (jsonify({
        "sentiments": sentiments,
        "tweets": my_tweets
    }))


app.run(host='0.0.0.0', debug=True)
