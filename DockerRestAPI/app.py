import os
import flask
import json
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import dateutil.parser as parser
import logging
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import logging

app = Flask(__name__)

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    distance = request.args.get('distance', type = int)
    begin_date = request.args.get('begin_date', type = str)
    begin_time = request.args.get('begin_time', type = str)
    dateAndTime = begin_date + " " + begin_time
    time = arrow.get(dateAndTime, 'YYYY-MM-DD HH:mm')  
    
    open_time = acp_times.open_time(km, distance, time.isoformat())
    close_time = acp_times.close_time(km, distance, time.isoformat())
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)



@app.route('/new', methods=['POST'])
def new():

    db.tododb.remove({}) #delete all entries in db upon new submission

    #error checking for km values. If all pass then appending to kmArray

    f = request.form
    distance = int(f['distance'])
    kmArray = []
    for value in f.getlist("km"):
        if(value != ""):
            floatValue = float(value)
            if(floatValue < 0):
                return flask.render_template('negative.html')
            elif(floatValue > 1000):
                return flask.render_template('max.html')    
            elif(floatValue > (distance * 1.2)):
                return flask.render_template('overtwenty.html')
            else:
                kmArray.append(value)
        else:
            break

    if(len(kmArray) == 0):
        return flask.render_template('error.html')
    #loop through all values of keys open and close and add to respective array
    openArray = getValues("open")
    closeArray = getValues("close")


    #create db entries with km distance, open and close times
    for i in range(len(kmArray)):
        # error check here for too fast of input
        item_doc = {
            'distance':request.form['distance'],
            'km': kmArray[i],
            'open':openArray[i],
            'close':closeArray[i]
        }
        db.tododb.insert_one(item_doc)

    return redirect(url_for('index'))


def getValues(key):
    #get all values based on keys from the submitted form
    f = request.form
    tempArray = []
    for value in f.getlist(key):
        if(value != ""):
            tempArray.append(value)
    return tempArray        





@app.route('/results', methods=['POST'])
def results():
    _items = db.tododb.find() #get all items in db
    items = [item for item in _items]
    if (len(items) == 0):
        return flask.render_template('error.html')
    return render_template('results.html', items=items)        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
