import numpy as np
import pandas as pd
import datetime as dt
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
    return jsonify(results)


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
    """Query the dates and temperature observations of the most active station for the last year of data. 
    Return a JSON list of temperature observations (TOBS) for the previous year."""
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    conn = engine.connect()
    session = Session(engine)
    ms_df = pd.read_sql('Select * from Measurement', conn)
    ms_df['total'] = 1
    activeStation_df = ms_df.groupby(['station']).sum().sort_values(by='total', ascending=False).reset_index()
    mostActiveStation = activeStation_df.iloc[0,0]
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date > '2016-08-23' ).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
@app.route("/api/v1.0/<start>") 
def temp_range(start, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    if end is not None:
        results = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start, Measurement.date <= end).label("TMIN"),
                            func.avg(Measurement.tobs).filter(Measurement.date >= start, Measurement.date <= end).label("TAVG"),
                            func.max(Measurement.tobs).filter(Measurement.date >= start, Measurement.date <= end).label("TMAX"))
        res = results.one()
        TMIN = res.TMIN
        TAVG = res.TAVG
        TMAX = res.TMAX
        session.close()
    elif end is None:
        results = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start).label("TMIN"),
                            func.avg(Measurement.tobs).filter(Measurement.date >= start).label("TAVG"),
                            func.max(Measurement.tobs).filter(Measurement.date >= start).label("TMAX"))
        res = results.one()
        TMIN = res.TMIN
        TAVG = res.TAVG
        TMAX = res.TMAX
        session.close()

    return (f'The minimum temperature for the given timeframe is {TMIN}.<br />'
            f'The approximate average temperature for the given timeframe is {round(TAVG,1)}.<br />'
            f'The maximum temperature for the given timeframe is {TMAX}.<br />')

if __name__ == '__main__':
    app.run(debug=True)