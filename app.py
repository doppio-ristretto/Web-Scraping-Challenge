from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import mars_scrape


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)


@app.route('/')
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

    
@app.route("/scrape")
def scraper():
    mars_data = mars_scrape.scrape()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

