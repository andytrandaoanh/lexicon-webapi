from flask import Flask, render_template
from flask import jsonify, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_cors import CORS
import mysql_connector as dbconn
from flask import request
from flask_pymongo import PyMongo
import handle_mysql as handleSQL
import handle_mongodb as handleMongo

#from flask_pymongo import ObjectId
from pprint import pprint


app = Flask(__name__)
CORS(app)
mysql = MySQL(cursorclass=DictCursor)
dbconn.set_conn_param(app)
mysql.init_app(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/lexicon"

mongo = PyMongo(app)

@app.route('/words')
def words():
	return handleSQL.fetchTopWords(mysql) 
		  #return 'hello world!'
@app.route('/query/<word>',  methods = ['GET'])
def query_word(word):
	if request.method == 'GET':
		return handleSQL.fetchAllWordsLike(mysql, word) 		

@app.route('/detail/<word>',  methods = ['GET'])
def detail_word(word):
	if request.method == 'GET':
		return handleMongo.fetchWordDetail(mongo, word)
		