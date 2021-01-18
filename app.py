import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)
# Flask Routes
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Convert the query results to a dictionary using date as the key and prcp as the value. Return the JSON representation of your dictionary."""
    # Query 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Convert list of tuples into normal list
    this_query = list(np.ravel(results))
    return jsonify(this_query)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of stations from the dataset."""
    # Query 
    results = session.query(Station.station).all()
    session.close()
    this_query = list(np.ravel(results))
    return jsonify(this_query)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    return f"to write later"
    """Query the dates and temperature observations of the most active station for the last year of data. 
    Return a JSON list of temperature observations (TOBS) for the previous year."""
    session.close()

@app.route("/api/v1.0/<start>")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    return f"to write later"
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def temp_range():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    return f"to write later"
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    session.close()

if __name__ == '__main__':
    app.run(debug=True)