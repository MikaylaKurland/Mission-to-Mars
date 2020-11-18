# Importing Dependencies
# use Flask to render a template.
from flask import Flask, render_template
# PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# use the scraping code
import Scraping
# Setting up Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up App Routes
# We will use 2 routes: one for the main HTML page everyone will view when visiting the web app, and one to actually scrape new data using the code we've written.

#defining the route for the HTML page
@app.route("/")
#index.html is the default HTML file that we'll use to display the content we've scraped
def index():
   # mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. 
   # We will also assign that path to themars variable for use later.
   mars = mongo.db.mars.find_one()
   # return render_template("index.html" tells Flask to return an HTML template using an index.html file.
   # mars=mars tells Python to use the "mars" collection in MongoDB.
   return render_template("index.html", mars=mars)

# defining the route for the scrape page - accessing the database, scraping for new data, updating our database, and returning a message if successful
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   # new variable to hold all data --> this is pulling from the "scrape all" function from scraping.py
   mars_data = Scraping.scrape_all()
   # update the database using update. see -> .update(query_parameter, data, options)
   # We're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter. 
   # Next, we'll use the data we have stored in mars_data. Finally, the option we'll include is upsert=True. 
   # This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()