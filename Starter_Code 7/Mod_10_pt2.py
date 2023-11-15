# Import the dependencies.
#from sqlachemy 
#from pathlib 
#import Path
#from sqlalchemy 

# Database Setup
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from pathlib import Path
import numpy as np
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Import Flask
from flask import Flask, jsonify
import datetime as dt

# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation" 
        f"/api/v1.0/stations"
        f"/api/v1.0/tob"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_years_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    last_years_precipitation = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= last_years_date).all()
    precipitation = {date: prcp for date, prcp in last_years_precipitation}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations_list():
    stations_list = session.query(station.station).all()
    stations_list = list(np.ravel(stations_list))
    return jsonify(stations=stations_list)

@app.route("/api/v1.0/tobs")
def most_active_station():
    most_active_station = session.query((measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    last_years_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    return jsonify(list(np.ravel(most_active_station)))
    

@app.route("/api/v1.0/temp/<start>")
def def_temp(start):
    start = dt.datetime.strptime(start, "%m%d%Y")
    temperature_range = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start).all()
    session.close()
    result = list(np.ravel(temperature_range))
    return jsonify(result)

@app.route("/api/v1.0/<start>/<end>")
def def_temp_range(start,end):
    start = dt.datetime.strptime(start,"%m%d%Y")
    end = dt.datetime.strptime(end,"%m%d%Y")
    temperature_range = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    result = list(np.ravel(temperature_range))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug= True)


