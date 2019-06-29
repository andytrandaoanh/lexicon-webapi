from flask import jsonify
from pprint import pprint

def fetch_data(mysql, query_statement):
	try:
		conn = mysql.connect()
		cursor =conn.cursor()

		cursor.execute(query_statement)
		data = cursor.fetchall()
		#resp = jsonify({"items": data})
		resp = jsonify(data)
		#code 200 means OK
		resp.status_code = 200 
		return  resp
	except Exception as e:
		print(e)
		resp.status_code = 400 
		return resp
	finally:		
		cursor.close() 
		conn.close()


def update_data(mysql, parameterizedSQL, dataTuple):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(parameterizedSQL , dataTuple)
		conn.commit()		
		resp  =  ("mysql sucessfully updated", 200)
		return resp
	except Exception as e:
		print(e)
		conn.rollback()
		resp  =  ("mysql update failed", 400) 
		return resp
	finally:		
		cursor.close() 
		conn.close()


def get_next_id(mysql, tableName, fieldName):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql_statement = "select MAX(" + fieldName + ") as max_id from " + tableName		
		cursor.execute(sql_statement)
		data = cursor.fetchone()
		new_id = data['max_id'] + 1 		
		return new_id
	except Exception as e:
		print(e)		 
		return null
	finally:		
		cursor.close() 
		conn.close()