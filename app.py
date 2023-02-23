import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-08-10<br/>"
        f"/api/v1.0/2017-08-10/2017-08-20"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of prcp values from last year"""
    # Query all prcp values from the last year date
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date> "2016-08-23").all()

    session.close()

   
    # Create a list of dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of temperature obseravtions of active station from last year"""
    # Query all temperature observations of active station from last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281" ).filter(Measurement.date> '2016-08-23' ).all()

    session.close()
    
    #Results the list of dictionary with date as key and tobs as value 
    active_station = []
    for date, tobs in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["tobs"] = tobs
        active_station.append(precipitation_dict)

    return jsonify(active_station)

@app.route("/api/v1.0/<start>")
def single_date(start):
    if start>="2010-01-01" and start <="2017-08-23":
        # Create our session (link) from Python to the DB
        session = Session(engine)
        
        sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]

        results = session.query(*sel).filter(Measurement.date >=start).all()

        # Close the Query
        session.close() 

        summary=[]
        for min,avg,max in results:
            summary_dict = {}
            summary_dict["tmin"] = min
            summary_dict["tavg"] = avg
            summary_dict["tmax"] = max
            summary.append(summary_dict)
        
        # Jsonify summary
        return jsonify(summary)
    else:
        return jsonify({"error": f"Date not in range, must be between 2010-01-01 and 2017-08-23."}), 404

@app.route("/api/v1.0/<start>/<end>")
def dates(start,end):
    
    if (start>="2010-01-01" and start <="2017-08-23") and (end >= "2010-01-01" and end <= "2017-08-23"):
        # Create our session (link) from Python to the DB
        session = Session(engine)
        
        sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]

        results = session.query(*sel).filter(Measurement.date >=start).all()

        # Close the Query
        session.close() 

        summary=[]
        for min,avg,max in results:
            summary_dict = {}
            summary_dict["tmin"] = min
            summary_dict["tavg"] = avg
            summary_dict["tmax"] = max
            summary.append(summary_dict)
        
        # Jsonify summary
        return jsonify(summary)
    else:
        return jsonify({"error": f"Date not in range, must be between 2010-01-01 and 2017-08-23."}), 404

        
if __name__ == '__main__':
    app.run(debug=True)