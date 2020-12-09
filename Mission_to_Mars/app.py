from flask import Flask, render_template
import time
from flask import Flask, render_template, redirect
from pymongo import MongoClient
import mission_to_mars

app = Flask(__name__)

mongo = MongoClient("mongodb://localhost:27017/mars_app")

@app.route("/")
def index():

    destination_data = mongo.db.collection.find_one()

    return render_template("index.html", mars_data=destination_data)


@app.route("/scrape")
def scrape():

    mars_data = mission_to_mars.mars_scraping()

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
