from flask import jsonify
from pprint import pprint

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




def processMeaning(meaning):
	#pprint(meaning)
	meaningList = []
	for key in meaning:
		objMeaning = {}
		objMeaning['category'] = key
		tempList = meaning[key]
		newList = []
		for item in tempList:
			tempObj = {}
			for k in item:
				if k == 'synonyms':
					syn_str = ', '.join(item[k])
					tempObj['synonyms'] = syn_str
				else:
					tempObj[k] = item[k]

			newList.append(tempObj)

		objMeaning['meaning'] = newList
		meaningList.append(objMeaning)
	#for item in meaningList:
	#	pprint(item)
	return meaningList

def processDoc(doc):
	#pprint(doc)
	wordList = []
	wordHeader = {}
	senseList = []
	for key in doc:
		if key == 'meaning':
			objMeaning = doc['meaning']
			senseList += processMeaning(objMeaning)
		else:
			wordHeader[key] = doc[key]

	#print('word header:', wordHeader)
	#print('sense list:', senseList)
	#print('length of sense list', len(senseList))
	for sense in senseList:
		wordObj = {}
		wordObj['category'] = sense['category']
		wordObj['meaning'] = sense['meaning']
		for key in wordHeader:
			wordObj[key] = wordHeader[key]
		
		wordList.append(wordObj)
	
	#pprint(wordList)

	return wordList

def unpackData(data):
	#purporse: flaten deeply-nested JSON data
	docList = []
	for doc in data:
		newDoc = {}
		for key in doc:
			if key !=  '_id':
				newDoc[key] = doc[key]
		docList.append(newDoc)	
	
	#dataOut = []
	
	#for doc in docList:
		#pprint(doc)
	#	dataOut += processDoc(doc)
	#return None
	return docList




def fetchGoogleDefinition(mongo, word):
	if (word):
		volumnName = 'google'
		collection = mongo.db[volumnName]
		data = collection.find({'word':word})
		docList = unpackData(data)

		#print('len:', len(docList))
		outList = []

		for doc in docList:
			outList += processDoc(doc)
			#pprint(wordList)
		resp = jsonify(outList)
		resp.status_code = 200
		return  resp
		#return ('hello', 200)
	else:
		resp = None
		resp.status_code = 400
	return  resp	