from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

#cretae an instance of flask 
app = Flask(__name__)

#Use pymongo to establish connection
mongo = PyMongo(app,uri="mongodb://localhost:27017/mars_app")

#Route to Render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    
    return render_template("index.html",data=mars_data)

                           
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_data()
    mongo.db.collection.update(
        {},mars_data,upsert=True)
    return redirect("/")
                           
if __name__ =="__main__":
   app.run(debug=True)                        
                               
                           