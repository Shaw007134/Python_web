from flask import Flask, request, flash, url_for, redirect, render_template,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
import pandas as pd
import numpy as np

host = '127.0.0.1'
port = 3306
db = 'egrid'
user = 'root'
password = 'root'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, password, host, db)
# app.config['SECRET_KEY'] = "secret key"

db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)


class Plants(db.Model):
  id = db.Column('index', db.Integer, primary_key = True)
  PSTAT = db.Column(db.String(10))
  PNAME = db.Column(db.String(200))
  PLNGENAN = db.Column(db.Float())
  CNTYNAME = db.Column(db.String(200))
  LAT = db.Column(db.Float())
  LON = db.Column(db.Float())
  YEAR = db.Column(db.Integer())


class PlantsSchema(ma.Schema):
  class Meta:
    fields = ("PNAME", "PSTAT", "PLNGENAN", "LAT", "LON")
    model = Plants

plant_schema = PlantsSchema()
plants_schema = PlantsSchema(many = True)


class States(db.Model):
  id = db.Column('index', db.Integer, primary_key = True)
  PSTAT = db.Column(db.String(10))
  STNGENAN = db.Column(db.Float())
  YEAR = db.Column(db.Integer())


class StatesSchema(ma.Schema):
  class Meta:
    fields = ("PSTAT", "STNGENAN")
    model = States

state_schema = StatesSchema()
states_schema = StatesSchema(many = True)


# @api.representation('text/html')
class PlantListResource(Resource):
    def get(self):
      plants = Plants.query.order_by(Plants.PLNGENAN.desc()).limit(100).all()
      headers = {'Content-Type': 'text/html'}
      return make_response(render_template('list_plants.html', Plants = plants_schema.dump(plants)),200,headers)

class StateListResource(Resource):
    def get(self):
      states = States.query.order_by(States.STNGENAN.desc()).limit(100).all()
      headers = {'Content-Type': 'text/html'}
      return make_response(render_template('list_states.html', States = states_schema.dump(states)),200,headers)



api.add_resource(PlantListResource, '/plants')
api.add_resource(StateListResource, '/states')


if __name__ == '__main__':
    app.run(debug=True)


