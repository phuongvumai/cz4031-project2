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
COLOR_WHEEL = ['#6992c2', '#ffdab9', '#fefcd7', '#fbea86', '#b66969', '#899b36']
tokens = None

def settokens(querytokens):
	global tokens
	tokens = querytokens
	cond_flag = 0
	for i in range(len(tokens)):
		print(i)
		words = [list(), list()]
		for word in tokens[i].split():
			word = word.strip(';').strip(',')
			if word in '=>=<=':
				cond_flag = 1
				words[1][len(words[1])-1]+= ' '+word
			elif cond_flag == 1:
				cond_flag = 0
				words[1][len(words[1])-1] += ' ' + word
			elif word.upper() == word:
				words[0].append(word)
			else:
				words[1].append(word)
		tokens[i] = words
	print(tokens)
def setqep(plan):
	global qep
	global graph
	qep = plan
	graph = pgv.AGraph(directed = True)
	creategraph(qep)
	exportgraph()

def exportgraph():
	graph.node_attr.update(shape='box', rank='same', style='filled')
	graph.graph_attr.update(rank='same', rankdir = 'BT')
	graph.layout()
	graph.draw('graph.gif', prog='dot')

def creategraph(node):
	if 'Plan' in node:
		return creategraph(node['Plan'])
	parent = Node(node)
	if 'Plans' in node:
	 	for item in node['Plans']:
	 		child = creategraph(item)
	 		graph.add_edge(child.nodeid, parent.nodeid)
	return parent


class Node:
	def __init__(self, node):
		global node_count
		self.nodeid = node_count
		node_count += 1
		self.label = "<"
		keywords_list = ['Key', 'Cond', 'Name']
		color = 'white'
		for attr in node.keys():
			if attr != 'Plans':
				self.label += html.escape(attr) + ": " + html.escape(str(node[attr]))
				self.label += "<BR/>"
			for keyword in keywords_list:
				if keyword in attr:
					for i in range(len(tokens)):
						for token in tokens[i][1]:
							if token in str(node[attr]):
								color = COLOR_WHEEL[i%len(COLOR_WHEEL)]

		self.label += ">"
		graph.add_node(self.nodeid, label = self.label, color = color)

