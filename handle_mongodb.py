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




def processGoogleMeaning(meaning):
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

def processGoogleDoc(doc):
	#pprint(doc)
	wordList = []
	wordHeader = {}
	senseList = []
	for key in doc:
		if key == 'meaning':
			objMeaning = doc['meaning']
			senseList += processGoogleMeaning(objMeaning)
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
			outList += processGoogleDoc(doc)
			#pprint(wordList)
		resp = jsonify(outList)
		resp.status_code = 200
		return  resp
		#return ('hello', 200)
	else:
		resp = None
		resp.status_code = 400
	return  resp	


def processLexiconMeanings(senses):
	#print('\n', senses)
	newSenseList = []
	newExampleList = []
	senseList = senses['senses']
	#print(senseList)\
	for senseObj in senseList:
		newObject = {}
		wordMeaning = ''
		wordVariant = ''
		crossReference = ''
		grammarNotes = ''
		regionDomain = ''
		wordRegister = ''
		highLight = ''
		exampleNumber = ''
		exampleMeaning = ''

		for key in senseObj:
			print('sense key:', key)
			if key == 'sense-number':
				newObject['number'] = senseObj[key]
				exampleNumber = senseObj[key]
			elif key == 'meaning':
				wordMeaning = senseObj[key]
				exampleMeaning = senseObj[key]

			elif key == 'spelling-variants':
				wordVariant = ' ' + senseObj[key] + ' '
			elif key == 'cross-reference':
				crossReference = ' ' + senseObj[key] + ' '
			elif key == 'grammer-notes':
				grammarNotes = ' [' + senseObj[key] + '] '
			elif key == 'region-domain':
				regionDomain = ' (' + senseObj[key].strip() + ') '	
			elif key == 'register':
				wordRegister = ' [' + senseObj[key].strip() + '] '	
			elif key == 'highlight':
				highLight = ' (' + senseObj[key].strip() + ') '	
			elif key == 'examples':
				newObject['example'] = senseObj[key][0]
				newExObj={}
				newExObj['number'] = exampleNumber + ' ' + exampleMeaning
				exampleNumber = ''
				exampleMeaning = ''
				newExObj[key] = senseObj[key]
				newExampleList.append(newExObj)
		
		newObject['meaning'] = wordVariant + crossReference + wordMeaning
		newObject['notes'] = grammarNotes + regionDomain + wordRegister + highLight

		newSenseList.append(newObject)

	return (newSenseList, newExampleList)

def processLexiconPhrases(phrases):
	#print(phrases)
	return []	

def processLexiconDoc(doc):
	#pprint(doc)
	
	
	wordHeader = {}
	wordFooter = {}
	wordMeanings = []
	moreExamples = []
	wordPhrases = {}
	headerCategoryList = []
	headerPhraseList = []
	headerFields = ('head-word', 'phonetic', 'spelling-variants', 'homograph-index', 'phonetic-transcripts')
	footerFields = ('word-origin', 'usage')
	phraseFields = ('phrases', 'phrases-verbs')

	for key in doc:
		
		print('\nkey:', key)
		if key in headerFields:
			wordHeader[key] = doc[key]
		elif key in footerFields:
			wordFooter[key] = doc[key]
		elif key in phraseFields:
			headerPhraseList.append(key)
		else:
			headerCategoryList.append(key)
			senseList, exampleList = processLexiconMeanings(doc[key])
			moreExamples += exampleList
			meaningObj = {'category': key, 'meanings': senseList}
			wordMeanings.append(meaningObj)

	wordHeader['categories'] = headerCategoryList
	wordHeader['phrases'] = headerPhraseList

	return {'header': wordHeader, 'meanings': wordMeanings, 'examples': moreExamples, 'phrases': wordPhrases,  'footer': wordFooter}


def fetchLexicoDefinition(mongo, word):
	if (word):
		volumnName = 'lexico'
		collection = mongo.db[volumnName]
		data = collection.find({'head-word':word})
		#pprint(data)
		docList = unpackData(data)
		#pprint(docList)

		outList = []

		for doc in docList:
			outList.append(processLexiconDoc(doc))
		resp = jsonify(outList)
		resp.status_code = 200
		return  resp
		#return('OK', 200)
	else:
		resp = None
		resp.status_code = 400
	return  resp	