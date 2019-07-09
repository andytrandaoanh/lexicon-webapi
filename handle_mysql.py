from mysql_data_process import fetch_data, update_data 
from mysql_data_process import fetch_raw_data, get_next_id
from pprint import pprint
from flask import jsonify


def getSentNumberForQuey(sentList):
	queryEnd = '('
	freshRun = True
	for item in sentList:
		if(freshRun):
			queryEnd += str(item['sent_num'])
			freshRun = False
		else:
			queryEnd += ',' + str(item['sent_num'])
	
	queryEnd += ')'	
	return queryEnd


def getQuotesByIndex(mysql, bookID, indexNumber):
	sql_statement = "select * from sentences where book_id = " + str(bookID) +  " and sent_num > " + str(indexNumber) + " LIMIT 6"
	list1 = fetch_raw_data(mysql, sql_statement)
	#print(data1)
	queryEnd = getSentNumberForQuey(list1)
	sql_statement = "select word_form, sent_num from mappings where book_id = " + str(bookID)  + " and sent_num in " + queryEnd + " order by book_id"
	list2 = fetch_raw_data(mysql, sql_statement)

	sql_statement = "select sword_form from stop_words"
	list3 = fetch_raw_data(mysql, sql_statement)
	stopWords = [item['sword_form'] for item in list3]
	sentList = []
	for item in list1:
		sentItem ={}
		sentItem['sent_id'] = item['sent_id']
		sentItem['sent_content'] = item['sent_content']
		sentItem['sent_num'] = item['sent_num']
		sentList.append(sentItem)
	

	wordList =  [w for w in list2  if w['word_form'].lower() not in stopWords]
	
	
	dataOut = {}
	dataOut['book_id'] = int(bookID)
	dataOut['sentences'] = sentList
	dataOut['words'] = wordList
	resp = jsonify(dataOut)
	resp.status_code = 200
	#print('sentList', sentList)

	return  resp	


def fetchDefaultQuotes(mysql, bookid):	
	sql_statement = "select * from sentences where book_id = " + str(bookid) + " LIMIT 2;"
	resp = fetch_data(mysql, sql_statement)
	return  resp




def fetchAllWordsLike(mysql, word):	
	sql_statement = "select * from pure_words where word_form like '" + word +"%' order by word_form;"
	resp = fetch_data(mysql, sql_statement)
	return  resp



def fetchTopWords(mysql):
	sql_statement = "select * from words order by word_form limit 100;"
	resp = fetch_data(mysql, sql_statement)
	return  resp

def fetchAllBooks(mysql):
	sql_statement = "select * from books order by book_id desc;"
	resp = fetch_data(mysql, sql_statement)
	return  resp

def saveBookEdit(mysql, data):
	#update books set book_title = 'The First-Time Manager', book_author = 'Loren B. Belke', book_year = 2012 where book_id = 1;
	parameterizedSQL = """update books set 
		book_title=%s, book_author=%s,
		book_year = %s where book_id = %s;"""
	dataTuple = (str(data['book_title']), str(data['book_author']), 
		int(data['book_year']), int(data['book_id']))
	resp = update_data(mysql, parameterizedSQL, dataTuple)
	return resp

def saveBookNew(mysql, data):
	#pprint(data)
	tableName = 'books'
	fieldName = 'book_id'
	newID = get_next_id(mysql, tableName, fieldName)
	parameterizedSQL = """insert into books (book_id, book_title, book_author, book_year) 
		VALUES(%s, %s, %s, %s)"""
	dataTuple = (newID, str(data['book_title']), str(data['book_author']), 
		int(data['book_year']))
	resp = update_data(mysql, parameterizedSQL, dataTuple)
	return resp