from flask import Flask, g, request
import random
import sqlite3
import datetime

app = Flask(__name__)

database = "ssrf.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ssrf (id INTEGER PRIMARY KEY AUTOINCREMENT, secret TEXT, timestamp TEXT, ip TEXT)")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def generateSecret():
    random_str = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    secret = ""

    for _ in range(0, 32):
        secret += random_str[random.randint(0, len(random_str) - 1)]

    return "SSRF-"+secret

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def secret(path):
    generated_secret = generateSecret()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    internal_ip = request.remote_addr
    cur = get_db().cursor()

    response = {
        "SSRF-Secret": generated_secret,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    cur.execute("INSERT INTO ssrf (secret, timestamp, ip) VALUES (?, ?, ?)", (generated_secret, timestamp, internal_ip))

    get_db().commit()

    return response, 200, {'Content-Type': 'application/json', 'SSRF-Secret': generated_secret}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)