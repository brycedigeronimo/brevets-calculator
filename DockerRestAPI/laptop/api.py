# Laptop Service

from flask import Flask, jsonify, Response
from flask_restful import Resource, Api, request
import os
import csv
import flask
from pymongo import MongoClient
import logging


# Instantiate the app
app = Flask(__name__)
api = Api(app)

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

class listAll(Resource):
    def get(self):
        return flask.jsonify(result = toJson("both"))   


class listOpenOnly(Resource):
    def get(self):
        #default for top argument is -1 which means no argument was given. Otherwise, return top x times
        args = request.args.get('top', -1, type = int)
        if(args >= 0):
            return flask.jsonify(result = topJson("open", args))
        else:
            return flask.jsonify(result = toJson("open"))

class listCloseOnly(Resource):
    def get(self):
        args = request.args.get('top', -1, type = int)
        if(args >= 0):
            return flask.jsonify(result = topJson("close", args))            
        else:
            return flask.jsonify(result = toJson("close"))

class listAllCsv(Resource):
    def get(self):
        bothTimes = toJson("both")
        csvWriter(bothTimes)
        csvfile = open('times.csv', 'r')
        return Response(csvfile, mimetype='text/csv')

class listOpenCsv(Resource):
    def get(self):
        args = request.args.get('top', -1, type = int)
        if(args >= 0):
            openTimes = topJson("open", args)            
        else:
            openTimes = toJson("open")
        csvWriter(openTimes)
        csvfile = open('times.csv', 'r')
        return Response(csvfile, mimetype='text/csv')


class listCloseCsv(Resource):
    def get(self):
        args = request.args.get('top', -1, type = int)
        if(args >= 0):
            closeTimes = topJson("close", args)
        else:
            closeTimes = toJson("close")
        csvWriter(closeTimes)
        csvfile = open('times.csv', 'r')
        return Response(csvfile, mimetype='text/csv')

# Create routes
# Another way, without decorators

def toJson(time):
    times = []
    _items = db.tododb.find()
    items = [item for item in _items]
    if(time == 'open'):
        for value in items:
            times.append({
                'open':value['open']
                })
    elif(time == 'close'):
        for value in items:
            times.append({
                'close':value['close']
                })
    elif(time == 'both'):
        for value in items:
            times.append({
                'open':value['open'],
                'close':value['close']
                })
    else:
        app.logger.debug("Enter a valid value")
    return times

def topJson(time, value):
    times = []
    _items = db.tododb.find()
    items = [item for item in _items]
    if(value > len(items)):
        value = len(items) #set value equal to number of times if top request is greater than number of items

    if(time == "open"):
        for x in range(value):
            times.append({
                'open':items[x]['open']
                })

    elif(time == "close"):
        for x in range(value):
            times.append({
                'close':items[x]['close']
                })
    else:
        app.logger.debug("please enter a valid value")
    return times

def csvWriter(time):
    file = open("times.csv", "w")
    writer = csv.writer(file)
    if(len(time) > 0):
        writer.writerow(time[0].keys())
    for item in time:
        writer.writerow(item.values())
    file.close()


api.add_resource(listAll, '/listAll', '/listAll/json')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/json')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/json')
api.add_resource(listAllCsv, '/listAll/csv')
api.add_resource(listOpenCsv, '/listOpenOnly/csv/')
api.add_resource(listCloseCsv, '/listCloseOnly/csv')


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
