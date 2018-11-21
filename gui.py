#!/usr/bin/env python3
import tkinter as tk
import queryhandler
from tkinter import ttk
from tkinter import messagebox
import visual
import codecs
import sqlparse
from PIL import Image, ImageTk

def main():
	root = tk.Tk()
	root.title('QEP Visual Explorer')
	maxwidth = root.winfo_screenwidth()
	maxheight = root.winfo_screenheight()
	root.geometry("%dx%d" %(maxwidth, maxheight))
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=5)
	root.rowconfigure(0, weight = 1)
	root.rowconfigure(0, weight=1)
	sidebar = SideBar(root)
	TreeView.setroot(root)
	root.mainloop()	

class Authenticate:
	def __init__(self):
		self.window = tk.Toplevel()	
		ttk.Label(self.window, text="DB name").grid(row = 0, sticky = 'nsew')
		self.dbname = tk.StringVar()
		ttk.Entry(self.window, textvariable=self.dbname).grid(row = 0, column = 1, sticky = 'nsew')
		ttk.Label(self.window, text="Username").grid(sticky = 'nsew')
		self.user = tk.StringVar()
		ttk.Entry(self.window, textvariable=self.user).grid(row = 1, column = 1, sticky = 'nsew')
		ttk.Label(self.window, text="Host").grid(sticky = 'nsew')
		self.host = tk.StringVar()
		ttk.Entry(self.window, textvariable=self.host).grid(row = 2, column = 1, sticky = 'nsew')
		ttk.Label(self.window, text="Password").grid(sticky = 'nsew')
		self.password = tk.StringVar()
		ttk.Entry(self.window, textvariable=self.password).grid(row = 3, column = 1, sticky = 'nsew')
		ttk.Button(self.window, text="Connect to Postgres DB", command = self.connect).grid(sticky = 'nsew')	
		for child in self.window.winfo_children(): 
			child.grid_configure(padx=5, pady=5)
	def connect(self):
		try:
			queryhandler.connect(self.dbname.get(), self.user.get(), self.host.get(), self.password.get())
			messagebox.showinfo("Authentication", "Postgres DB connected")
			self.window.destroy()
		except Exception as err:
			print(err)
			messagebox.showinfo("Authentication", "Authentication fails. Make sure the database server is on and credentials are correct.")

class SideBar:
	def __init__(self, root):
		self.frame = ttk.Frame(root, borderwidth=4, relief='groove')
		self.frame.grid(row=0, column = 0, sticky = "nsew")
		self.frame.columnconfigure(0, weight=1)
		ttk.Button(self.frame, text="Connect to Postgres DB", command = self.auth).grid(sticky = 'nsew')	
		ttk.Button(self.frame, text="Disconnect from Postgres DB", command = self.disconnect).grid(sticky = 'nsew')	
		ttk.Label(self.frame, text="Enter SQL query").grid(sticky = 'nsew')
		self.query = tk.StringVar()
		entry = ttk.Entry(self.frame, textvariable=self.query)
		entry.grid(sticky = 'nsew', rowspan=3)	
		ttk.Button(self.frame, text="Explain SQL query", command = self.explain).grid(sticky = 'nsew')	
		ttk.Button(self.frame, text="Compare").grid(sticky = 'nsew')
		ttk.Button(self.frame, text="Clear").grid(sticky = 'nsew')
		for row_num in range(self.frame.grid_size()[1]):
			self.frame.rowconfigure(row_num, minsize=60)
		entry.focus()
		for child in self.frame.winfo_children(): 
			child.grid_configure(padx=5, pady=5)
	def explain(self):
		try:
			sqlquery = self.query.get()
			qep = queryhandler.explain(codecs.unicode_escape_decode(sqlquery)[0])
			tokens = sqlparse.format(sqlquery, reindent=True).split('\n')
			for i in range(len(tokens)):
				tokens[i] = tokens[i].strip()
			visual.settokens(tokens)
			TreeView.img.configure(image='')
			TreeView.img.image = ''
			visual.setqep(qep[0][0][0])
			TreeView.refresh()
		except Exception as err:
			print(err)
			messagebox.showinfo("SQL query", "SQL query incorrect or DB disconnected.")
	def auth(self):
		self.auth = Authenticate()
	def disconnect(self):
		try:
			queryhandler.disconnect()
		except Exception as err:
			print(err)
			messagebox.showinfo("Connection", "Postgres DB fails to disconnect. Are you sure the DB is connected?")
class TreeView:
	def setroot(root):
		canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
		TreeView.frame = tk.Frame(canvas, background="#ffffff")
		vsb = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
		vsb_h = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
		canvas.configure(yscrollcommand=vsb.set)
		canvas.configure(xscrollcommand=vsb_h.set)
		vsb.grid(row=0, column=2, sticky='ns')
		vsb_h.grid(row=1, column=1, sticky='ew')
		canvas.grid(row=0, column = 1, sticky='nsew')
		canvas.create_window((4,4), window=TreeView.frame, anchor="nw")
		TreeView.frame.bind("<Configure>", lambda event, canvas=canvas: TreeView.onFrameConfigure(canvas))
		TreeView.img = ttk.Label(TreeView.frame)
		TreeView.img.grid()
		TreeView.canvas = canvas

	def refresh():
		photo = ImageTk.PhotoImage(Image.open('graph.gif'))
		TreeView.img.configure(image=photo)
		TreeView.img.image = photo
		print(TreeView.frame.grid_size())
		print(TreeView.canvas.winfo_height())
		print(TreeView.canvas.winfo_width())
		print(TreeView.frame.winfo_height())
		print(TreeView.frame.winfo_width())
	def onFrameConfigure(canvas):
		canvas.configure(scrollregion=canvas.bbox("all"))
if __name__ == '__main__':
	main()