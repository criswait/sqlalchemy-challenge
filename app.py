# Import the dependencies.

from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#################################################
# Database Setup
#################################################
#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Homepage route
@app.route('/')
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt; (e.g., /api/v1.0/2017-01-01)<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; (e.g., /api/v1.0/2017-01-01/2017-12-31)<br/>"
    )

# Precipitation data route
@app.route('/api/v1.0/precipitation')
def precipitation():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date_dt = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date_dt - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= one_year_ago).all()

    precipitation_dict = {date: prcp for date, prcp in results}
    return jsonify(precipitation_dict)

# Stations data route
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

# Temperature observations route
@app.route('/api/v1.0/tobs')
def tobs():
    most_active_station_id = session.query(
        Measurement.station).group_by(
        Measurement.station).order_by(
        func.count(Measurement.station).desc()).first()[0]

    last_12_months_temps = session.query(Measurement.tobs).filter(
        Measurement.station == most_active_station_id,
        Measurement.date >= one_year_ago
    ).all()

    temps_list = [temp[0] for temp in last_12_months_temps]
    return jsonify(temps_list)

# Temperature stats by date range route
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temperature_stats(start, end=None):
    if end:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).all()

    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)