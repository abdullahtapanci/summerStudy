from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#api requirements
API_KEY = "97b8da01-f4b6-4f4c-b8c0-b0070d634cc0"
headers = {
    'X-CMC_PRO_API_KEY': API_KEY,
    'Accepts': 'application/json',
    'Accept-Encoding': 'deflate, gzip',
}
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
#id=1 is equal to symbol=BTC
params = {
    'id': '1'
}

bitcoinData=0

@app.route("/")
def mainPage():
    return render_template('index.html')

def getData():
    global bitcoinData
    try: 
        response = requests.get(url, headers=headers, params=params)

        data = response.json()
        bitcoinData = data['data']['1']

        try:
            with open("../BTCData/btcData.csv", "a") as f:
                f.write(
                    str(bitcoinData["id"]) + "," +
                    bitcoinData['name'] + "," +
                    bitcoinData['symbol'] + "," +
                    str(bitcoinData['quote']['USD']['price']) + "," +
                    str(bitcoinData['circulating_supply']) + "," +
                    str(bitcoinData['quote']['USD']['market_cap']) + "," +
                    str(bitcoinData['quote']['USD']['volume_24h']) + "," +
                    str(bitcoinData['quote']['USD']['percent_change_24h']) + "," +
                    str(bitcoinData['last_updated']) + "\n"
                )
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        

@socketio.on("connection")
def connect():
    print("Client connected")
    while True:
        getData()
        emit("data", {"data": bitcoinData }, broadcast=True)
        time.sleep(10)

    


if __name__ == '__main__':
    socketio.run(app, debug=True)

