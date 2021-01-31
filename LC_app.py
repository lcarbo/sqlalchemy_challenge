import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measures = Base.classes.measurement
station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def home(): 
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    oneyr_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    precip_result=session.query(measures.date, measures.prcp).filter(measures.date >= oneyr_ago).order_by(measures.date.asc()).all()
    session.close()

    precip_list= []
    
    for date, prcp in precip_result: 
        precip_dict={}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict) 

    return jsonify(precip_list)



@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    station_result=session.query(measures.station).distinct().all()
    session.close()

    station_list= []
    
    for each in station_result: 
        station_list.append(each)  

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    oneyr_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    active_annual = session.query(measures.date, measures.tobs).filter(measures.station =='USC00519281').filter(measures.date >= oneyr_ago).order_by(measures.date.asc()).all()

    session.close()

    active_list = []
    
    for date, tobs in active_annual: 
            active_dict={}
            active_dict["date"] = date
            active_dict["tobs"] = tobs
            active_list.append(active_dict) 

    return jsonify(active_list)

@app.route("/api/v1.0/<start_date>")
@app.route("/api/v1.0/<start_date>/<end_date>")
def date_range(start_date= none, end_date= none):

    stats = [func.min(measures.tobs), func.avg(measures.tobs), func.max(measures.tobs)]

    if end == none: 
        range_results = session.query(*stats).filter(measures.date >= start_date).all()
    range_tobs = list(np.ravel(range_results))
    return jsonify (range_tobs)




    



if __name__ == "__main__":
    app.run(debug=True)