#!/urs/bin/env python3

import pygraphviz as pgv
import json
import codecs
import html

FILE = 'qep.json'
PNG = 'qep.png'
qep = None
graph = None
node_count = 0
COLOR_WHEEL = ['6992c2', '#ffdab9', '#fefcd7', '#fbea86', '#b66969', '#899b36']
tokens = None

def settokens(querytokens):
	global tokens
	tokens = querytokens

def setqep(plan):
	global qep
	global graph
	qep = plan
	# # with open(FILE, 'w') as outfile:
	# # 	json.dump(qep, outfile)
	# with open(FILE, 'r') as outfile:
	#  	qep = json.load(outfile)
	graph = pgv.AGraph(directed = True)
	creategraph(qep)
	exportgraph()

def exportgraph():
	graph.node_attr.update(shape='box', rank='same', style='filled')
	graph.graph_attr.update(rank='same', rankdir = 'TB')
	graph.layout()
	graph.draw('graph.gif', prog='dot')

def creategraph(node):
	if 'Plan' in node:
		return creategraph(node['Plan'])
	parent = Node(node)
	if 'Plans' in node:
	 	for item in node['Plans']:
	 		child = creategraph(item)
	 		graph.add_edge(parent.nodeid, child.nodeid)
	return parent


class Node:
	def __init__(self, node):
		global node_count
		self.nodeid = node_count
		node_count += 1
		self.label = "<"
		for attr in node.keys():
			if attr != 'Plans':
				self.label += html.escape(attr) + ": " + html.escape(str(node[attr]))
				self.label += "<BR/>"
		self.label += ">"
		graph.add_node(self.nodeid, label = self.label)

