from flask import Flask
import os 
app = Flask(__name__)

@app.route("/")
def home():
    return("Smart Fashion Recommender")

if __name__=="__main__":
    port = os.environ.get("PORT",5000)
    app.run(debug = True, port=port,host="0.0.0.0")
