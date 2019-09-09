from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
import scrape_mars

# #################################################
# # Setup Dictionary of Mars_data
# #################################################
db_nasa = [
    {"news title": "news_title", "news article": "news_p"}
]

db_twitter = [
    {"Weather_Notes": "Mars missions go silent during solar conjunction: https://www.wral.com/mars-spacecraft-go-quiet-during-solar-conjunction/18595551/ …pic.twitter.com/fWruE2v151report"},
    {"Current_Weather_Report": "InSight sol 265 (2019-08-25) low -99.4ºC (-146.9ºF) high -26.3ºC (-15.3ºF)/"
                               "winds from the SSE at 5.3 m/s (12.0 mph) gusting to 16.1 m/s (35.9 mph)/"
                               "pressure at 7.50 hPapic.twitter.com/9YLawm67zS" }
]

featured_image = [
    {"featured_image": "https://www.jpl.nasa.gov /spaceimages/images/largesize/PIA18452_hires.jpg"}
]

mars_earth_comparision = [
    {"ID": "1", "Mars Diameter": "6,779 km", "Earth Diameter": "12,742 km"},
    {"ID": "2", "Mars Mass": "6.39 × 10^23 kg", "Earth Mass": "5.97 × 10^24 kg"},
    {"ID": "3", "Mars Moons": "2", "Earth Moons": "1"},
    {"ID": "4", "Mars Distance from Sun": "227,943,824 km", "Earth Distance from Sun": "149,598,262 km"},
    {"ID": "5", "Mars Length of Year": "687 Earth days", "Earth Length of Year": "365.24 days"},
    {"ID": "6", "Mars Temperature": "-153 to 20 °C", "Earth Temperature": "-88 to 58°C"},
    {"ID": "7", "Mars Equatorial Diameter": "6,792 km (0.5 Earths)"},
    {"ID": "8", "Mars Polar Diameter": "6,792 km"},
    {"ID": "9", "Mars Mass": "6.39 × 10 ^ 23kg or (0.11 Earths)"},
    {"ID": "10", "Mars Moons Names": "Phobos & Deimos", "Earth Moon Name": "Moon"},
    {"ID": "11", "Mars Orbit Distance": "227, 943, 824 km(1.38 AU)"},
    {"ID": "12", "Mars Orbit Period": "687 days(1.9 years)"},
    {"ID": "13", "Mars Surface Temperature": "-87 to -5°C"},
    {"ID": "14", "Mars First Record": "2nd millennium BC by Egyptian Astronomer"}
]

hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"}
]

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)

# #################################################
# # Connect to Mongodb
# #################################################
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to collections created in jupyter notebook.
db = nasa_db


# Drops collection if available to remove duplicates
# db.nasa.drop()
# db.twitter.drop()

#################################################
# Flask Routes
#################################################
# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)

# @app.route('/')
# def index():
#
#     # Store the entire mars news collection in a list
#     mars = list(db.nasa.find(news_title, news_p))
#     print(mars)
#
#     # Return the template with the news passed in
#     return render_template('index.html', mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


