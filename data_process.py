from flask import jsonify


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
