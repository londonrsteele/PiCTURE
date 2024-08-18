# Filename : server.py
# Author   : LR Steele
# Descrptn : Flask server for React app
from flask import Flask

# Initialize app
app = Flask(__name__)

# One route for api
@app.route("/home")
def say_hello():
    # return an api
    return {
        "Greeting": "Hello, ",
        "Name": "London!"
    }

# Running app
if __name__ == "__main__":
    app.run(debug=True)