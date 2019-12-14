import sqlite3 as sql
import pandas as pd

def openDatabase(filename):
	return sql.connect(filename)

def writeTable(tableName, connection, dataFrame):
	dataFrame.to_sql(tableName, connection, index=False)

def updateTable(tableName, dataFrame):
	dataFrame.to_sql(tableName, connection, index=False, if_exists='replace')

def tableExists(tableName, connection):
	return pd.io.sql.has_table(tableName, connection)

def readTable(tableName, connection):
	return pd.read_sql("SELECT * from " + "'" + tableName + "'", connection)

def writeFile(tableName, connection, fileData):
	connection.execute('CREATE TABLE ' + tableName + ' (thebin BLOB)' )
	connection.execute('INSERT INTO ' + tableName + ' VALUES(?)', [buffer(fileData)] )

def readFile(tableName, connection, toTemporaryFile=False):
	row = connection.execute('SELECT * FROM ' + tableName).fetchone()
	restored = str(row[0])

	if toTemporaryFile is False:
		return restored
	else:
		import tempfile
		with tempfile.NamedTemporaryFile(delete=False) as temp:
			temp.write(restored)
			return temp.name