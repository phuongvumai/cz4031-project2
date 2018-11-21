#!/usr/bin/env python3

import psycopg2

conn = None
cur = None
def connect(DBNAME, USER, HOST, PASSWORD):
	try:
		global conn
		global cur
		conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" %(DBNAME, USER, HOST, PASSWORD))
		cur = conn.cursor()
		global authflag
		print("Connection opened")
	except Exception as err:
		raise err
def disconnect():
	try:
		cur.close()
		conn.close()
		print("Connection closed")
	except Exception as err:
		print(err)
		raise err
def explain(query):
	query = 'EXPLAIN (format json) ' + query
	print(query)
	try:
		cur.execute(query)
		return(cur.fetchall())
	except Exception as err:
		conn.rollback()	
		raise err