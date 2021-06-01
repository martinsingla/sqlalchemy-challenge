## FLASK API APP

#Dependencies
from numpy.lib.function_base import average
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect= True)
Station = Base.classes.station
Measurement = Base.classes.measurement

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
        f'/api/v1.0/Start_date:start_date   (YYYY-MM-DD) <br/>'
        f'/api/v1.0/Start_date:start_date/End_date:end_date  (YYYY-MM-DD)'
    )

#Precipitations
@app.route("/api/v1.0/precipitation")
def prcp():
    print('Access precipitations page')
  
    session = Session(engine)
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    session.close()

    prcp_historic = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_historic.append(prcp_dict)

    return jsonify(prcp_historic)

#Stations
@app.route("/api/v1.0/stations")
def stations():
    print('Access to stations page')

    session = Session(engine)
    stations_query = session.query(Station.station, Station.name).all()
    session.close()

    stations_list = []
    for station, name in stations_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations_list.append(station_dict)
    
    return jsonify(stations_list)

#Temperatures at Most Active Station for last year of data
@app.route("/api/v1.0/tobs")
def tobs():
    print('Accessing tops page')

    session = Session(engine)
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281', Measurement.date > '2016-08-17').all()
    session.close()

    tobs_list = []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)

#Temperature Start
@app.route("/api/v1.0/Start_date:<start_date>")
def start(start_date):

    session = Session(engine)
    start_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > start_date)
    session.close()
    
    tobs = []; 
    for i in start_query: tobs.append(i[1])
    tobs_dict = {'Min': min(tobs), 'Max': max(tobs), 'Avg': average(tobs)}

    return jsonify(tobs_dict)

#Temperature Start / End
@app.route('/api/v1.0/Start_date:<start_date>/End_date:<end_date>')
def start_end(start_date, end_date):

    session = Session(engine)
    start_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > start_date, Measurement.date < end_date)
    session.close()
    
    tobs = []; 
    for i in start_query: tobs.append(i[1])
    tobs_dict = {'Min': min(tobs), 'Max': max(tobs), 'Avg': average(tobs)}

    return jsonify(tobs_dict)

#Run APP
if __name__ == "__main__":
    app.run(debug=True)