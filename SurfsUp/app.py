# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Set the autoload_with separately
Base.prepare(engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Start at the homepage.
@app.route("/")
def welcome():
    #List all the available api routes.
    return (
        f"Welcome to the Climate App! Please see available routes below:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

# PRECIPITATION
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the database.
    session = Session(engine)

    # Query precipitation.
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    session.close()
    
    # Convert the query results from the precipitation analysis to a dictionary.
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    # Return a JSON representation of the dictionary.
    return jsonify(all_prcp)

# STATIONS
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the database.
    session = Session(engine)

    # Query stations.
    results = session.query(Station.station).\
                 order_by(Station.station).all()

    # Close the session.
    session.close()

    # Convert list of tuples into normal list.
    all_stations = list(np.ravel(results))

    # Return a JSON list of stations from the dataset.
    return jsonify(all_stations)


# TOTAL OBSERVATIONS
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Query dates and temperatures of the most-active station for the previous year of data.
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station == 'USC00519281').\
                order_by(Measurement.date).all()

    session.close()
    
    # Convert the list to Dictionary
    all_tobs = []
    for date, tobs in results:  # Corrected the unpacking of results
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    # Return a JSON list of temperature observations
    return jsonify(all_tobs)

# TEMPERATURES START
@app.route("/api/v1.0/start/<start_date>")
def Start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query min, avg, and max temperatures for the date range starting from start_date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary to hold the results
    start_date_tobs = []
    for min_temp, avg_temp, max_temp in results:
        start_date_tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_date_tobs.append(start_date_tobs_dict)

    # Return a JSON list of min, max, and average temps from the start date to the end of the dataset.
    return jsonify(start_date_tobs)

# TEMPERATURES START TO END
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Query min, avg, and max temperatures for the date range between start_date and end_date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    session.close()
    
    # Create a dictionary to hold the results
    start_end_tobs = []
    for min_temp, avg_temp, max_temp in results:
        start_end_tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_end_tobs.append(start_end_tobs_dict) 
    
    # Return a JSON list of min, max, and average temps for the date range.
    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)