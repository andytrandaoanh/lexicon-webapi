from flask import jsonify

def fetchWordDetail(mongo, word):
	if (word):
		volumnName = 'vol_' +  word[:1].lower()
		collection = mongo.db[volumnName]
		data = collection.find({'key_word':word})
		output = []
		for doc in data:
			output.append({'book_id': doc['book_id'], 'book_title': doc['book_title'], 'book_author': doc['book_author'],'book_year': doc['book_year'],  'key_word' : doc['key_word'], 'sent_content' : doc['sent_content'], 'sent_num': doc['sent_num']})
		resp = jsonify(output)
		resp.status_code = 200
		return  resp
	else:
		resp = None
		resp.status_code = 400
	return  resp