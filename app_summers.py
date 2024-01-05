# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# Create an SQLAlchemy engine
engine = create_engine("sqlite:///C:/Users/ianro/OneDrive/Documents/Bootcamp/UofU-VIRT-DATA-PT-10-2023-U-LOLC/10-Advanced-SQL/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite"
)

# Reflect an existing database into a new model and reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of precipitation data."""
    # Calculate the date one year ago from the most recent date in the dataset
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp) \
        .filter(Measurement.date >= one_year_ago) \
        .all()

    # Convert the results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

# Define other routes (stations, tobs, <start>, and <start>/<end>) similarly

# Add if __name__ == "__main__" block to run the app if executed as a standalone script
if __name__ == "__main__":
    app.run(debug=True)