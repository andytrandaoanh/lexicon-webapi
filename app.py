from flask import Flask, render_template
from flask import jsonify, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_cors import CORS
import dbconn
from flask import request
from data_process import fetch_data
from flask_pymongo import PyMongo

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
	sql_statement = "select * from words order by word_form limit 100;"
	resp = fetch_data(mysql, sql_statement)
	return  resp
		  #return 'hello world!'
@app.route('/query/<word>',  methods = ['GET'])
def query_word(word):
	if request.method == 'GET':
		sql_statement = "select * from pure_words where word_form like '" + word +"%' order by word_form;"
		resp = fetch_data(mysql, sql_statement)
		return  resp 		

@app.route('/detail/<word>',  methods = ['GET'])
def detail_word(word):
	if request.method == 'GET':

		if (word):
		#print(doc['key_word'])
			volumnName = 'vol_' +  word[:1].lower()
			#print ('volume name', volumnName)
			collection = mongo.db[volumnName]
			#print('collection: ', collection)
	
			data = collection.find({'key_word':word})
			#print('search data:', data)
			output = []
			for doc in data:
				#str_obj = ObjectID.str(doc[0])
				#print (str_obj)

				output.append({'book_id': doc['book_id'], 'book_title': doc['book_title'], 'book_author': doc['book_author'],'book_year': doc['book_year'],  'key_word' : doc['key_word'], 'sent_content' : doc['sent_content'], 'sent_num': doc['sent_num']})
			 
			resp = jsonify(output)
			#code 200 means OK
			resp.status_code = 200 
			return  resp 		
		else:
			resp = None
			resp.status_code = 400 
			return  resp 