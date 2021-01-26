import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    precip_result=session.query(measures.date, measures.prcp).all()
    session.close()

    precip_list= []
    
    for date, prcp in precip_result: 
        precip_dict={}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict)

    return jsonify(precip_dict)

if __name__ == "__main__":
    app.run(debug=True)