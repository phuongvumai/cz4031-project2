#!/usr/bin/env python3

import psycopg2

DBNAME = 'phuongvu'
USER = 'phuongvu'
HOST = 'localhost'
PASSWORD = 'password'
conn = None
cur = None
def connect():
	try:
		global conn
		global cur
		conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" %(DBNAME, USER, HOST, PASSWORD))
		cur = conn.cursor()
		print("Connection opened")
	except:
		print("Wrong credentials")
def close():
	conn.commit()
	cur.close()
	conn.close()
	print("Connection closed")
def explain():
	query = input()
	while(query != 'exit'):
		query = 'EXPLAIN (format json) ' + query
		try:
			cur.execute(query)
			print(cur.fetchall())
		except:		
			print("Invalid command")
			break
		query = input()