#!/usr/bin/env python3

from flask import Flask 
from model.orm import ORM
from data.schema import DBPATH

ORM.dbpath = DBPATH #do i need to import from somewhere else?

app = Flask(__name__) #YOU ALWAYS DO THIS | STANDARD FLASK APPS ARE INITIALIZED THIS WAY

#circular imports --> we are importing routes below, in routes we are importing app
from . import routes #NOTE THAT THIS IS HERE (BELOW app = Flask(__name__)) ON PURPOSE because of circular imports

