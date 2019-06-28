from data_process import fetch_data


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