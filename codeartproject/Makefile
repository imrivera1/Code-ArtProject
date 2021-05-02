
# Creates the database if database is reset ( or cleaned ) or if it is being created for the first time
app_setup:
	python projectFiles/initialization/init_db.py

# Creates an admin account using the hardcoded credentials in the file
# The credentials must be changed for each individual account before running this command
admin_cred:
	python projectFiles/initialization/admin_credentials.py

# Sets up the flask application and environment and runs it
flask:
	FLASK_APP=projectFiles/database.py FLASK_ENV=development python -m flask run --port 4258

# Resets the database if there was an error or glitch causing it to need to be reset
# Be careful, all information stored in the database, including admin accounts, will be erased 
clean:
	rm projectFiles/databaseFiles/ca_database.db
	touch projectFiles/databaseFiles/ca_database.db