## FLASK API APP

#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect= True)
station = Base.classes.station
measurement = Base.classes.measurement

#Flask Setup
app = Flask(__name__)

#Home
@app.route("/")
def home():
    print('Access API home page')

    return (
        f'Available routes: <br/>'
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/start <br/>'
        f'/api/v1.0/start/end'
    )

#Precipitations
@app.route("/api/v1.0/precipitation")
def prcp():
    print('Access precipitations page')
  
    session = Session(engine)
    prcp_results = session.query(measurement.date, measurement.prcp).\
        order_by(measurement.date).all()
    session.close()

    prcp = list(np.ravel(prcp_results))
    return jsonify(prcp)

#Stations
@app.route("/api/v1.0/stations")
def stations():
    print('Access precipitations page')
    
    session = Session(engine)
    stations_results = session.query(station.station, station.name).\
        order_by(station.station).all()
    session.close()

    stations = list(np.ravel(stations_results))
    return jsonify(stations)

#Temperature most active station
@app.route("/api/v1.0/tobs")
def precipitations():
    print('Access precipitations page')

    session = Session(engine)
    tobs_results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-22',measurement.station =="USC00519281" ).\
        order_by(measurement.date).all()
    session.close()

    tobs= list(np.ravel(tobs_results))
    return jsonify(tobs)

#Temperature Start
@app.route("/api/v1.0/start")
def start():
    print('Access start page')

    session = Session(engine)
    date_start = dt.datetime(2012, 5, 4)
    stats= [func.min(measurement.tobs), 
    func.max(measurement.tobs), 
    func.avg(measurement.tobs)] 

    start_results = session.query(*stats).\
        filter(measurement.date > date_start ).\
        order_by(measurement.date).all()

    session.close()
    start_stats= list(np.ravel(start_results))

    return jsonify(start_stats)

#Temperature Start / End
@app.route("/api/v1.0/start/end")
def start_end():
    print('Access start end page')

    session = Session(engine)
    date_start = dt.datetime(2012, 5, 4)
    date_end = dt.datetime(2014, 5, 4)
    stats= [func.min(measurement.tobs), 
    func.max(measurement.tobs), 
    func.avg(measurement.tobs)] 

    start_end = session.query(*stats).\
        filter(measurement.date >= date_start).\
        filter(measurement.date <= date_end).\
        order_by(measurement.date).all()
    session.close()

    start__end_stats= list(np.ravel(start_end))
    return jsonify(start__end_stats)

#Run APP
if __name__ == "__main__":
    app.run(debug=True)