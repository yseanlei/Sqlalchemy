import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
lastdate=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
ltm=dt.date(int(lastdate[0][:4]),int(lastdate[0][5:7]),int(lastdate[0][8:11]))-dt.timedelta(days=365)
preci=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>ltm).filter(Measurement.date<lastdate[0]).all()
allstation=session.query(Measurement.station.distinct()).all()
tem=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>ltm).filter(Measurement.date<lastdate[0]).all()

app=Flask(__name__)

@app.route("/")
def home():
    return(f"Welcome to the weather homepage, please use the following addresses for API query:<br/>"
      f'For precipitation:<br/>"/api/v1.0/precipitation"<br/>'
      f'For station:      <br/>"/api/v1.0/stations"<br/>'
      f'For temperature:  <br/>"/api/v1.0/tobs"<br/>'
      f'For highest, average and lowest temperatures of the period after a certain date:<br/>"/api/v1.0/<start>"<br/>'
      f'For highest, average and lowest temperatures of the period between two specified dates:<br/>"/api/v1.0/<start>/<end>"<br/>'
      f'Please note: Date format needs to be "yyyy-mm-dd", otherwise query will not be processed <br/>'
      f'The API accepts data query for dates between "2016-08-23" and "2017-08-23"')
@app.route("/api/v1.0/precipitation")
def precipitation():
    precidict={}
    for p in preci:
        precidict[p[0]]=p[1]
    return jsonify(precidict)
@app.route("/api/v1.0/stations")
def station():
    return jsonify(allstation)
@app.route("/api/v1.0/tobs")
def temp():
    temperature={}
    for t in tem:
        temperature[t[0]]=t[1]
    return jsonify(temperature)
@app.route("/api/v1.0/<start>")
def start_temp(start):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    tempdata=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date>=start).all()
    return jsonify(tempdata)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    setempdata=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
                .filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    return jsonify(setempdata)

if __name__ == "__main__":
    app.run(debug=True)