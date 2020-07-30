from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
