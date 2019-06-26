def set_conn_param(app):
	app.config['MYSQL_DATABASE_USER'] = 'webuser'
	app.config['MYSQL_DATABASE_PASSWORD'] = 'DGweb#1234'
	app.config['MYSQL_DATABASE_DB'] = 'lexicon'
	app.config['MYSQL_DATABASE_HOST'] = 'localhost'
	