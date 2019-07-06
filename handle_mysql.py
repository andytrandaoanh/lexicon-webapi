from mysql_data_process import fetch_data, update_data, get_next_id
from pprint import pprint



def fetchDefaultQuotes(mysql, bookid):	
	sql_statement = "select * from sentences where book_id = " + str(bookid) + " LIMIT 5;"
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