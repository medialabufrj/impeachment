# coding: utf-8
from gdflib import GdfEntries, Node
import csv
import re

entities = GdfEntries()
links = dict()

def strip_digits(s):
    return re.sub("\d+", "", s)

def removeWords(w):
	return w.lower() not in ["-","—",",",".","%",":","sr","srs","sra","sras","v.exa","a","o","as","os","e","do","da","de","dos","das","na","no","nas","nos","com","quem","um","uma","uns","umas","esta","essa","este","esse","estas","essas","estes","esses","isso","isto","em","para","se","mas","ou","que","ao","à","aos","às","até","por","portanto","pelo","pelos","pela","pelas","sua","suas","seu","seus","ali","aqui","é","tem","são","foi","está","vai","era","tinha","tendo","palmas","já"]

def removePonctuations(w):
	w = w.replace("...", "")
	w = w.replace("(", "")
	w = w.replace(")", "")
	if len(w) > 1:
		last = w[-1]
		if last in ".,;:!?%":
			#print(['last is:',last, w])
			return w[:-1]
	return w

def link(node1, node2, w):
	key = node1 + "_" + node2
	if key in links:
		links[key] += w
	else:
		links[key] = w


with open('discursos-impeachment.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	count = 0
	for row in reader:

		count += 1
		print(["processing", count])

		party = row['Partido'].decode('utf-8')

		phrase = row['Fala'].decode('utf-8')
		phrase = strip_digits(phrase)
		phrase = sorted(phrase.split(' '))
		phrase = list(map(removePonctuations, phrase))
		phrase = [x.lower() for x in phrase]
		phrase = list(filter(removeWords, phrase))
		phrase = list(filter(None, phrase))

		entities.add_node(Node(name=party, label=party))
		
		print(phrase)
		for word in phrase:
			entities.add_node(Node(name=word, label=word))
			for other_word in phrase:
				if word != other_word:
					entities.add_node(Node(name=other_word, label=other_word))
					link(word, other_word, 0.1)
					link(party, word, 1)

for k, v in links.iteritems():
	nodes = k.split('_')
	if v > 0.3:
		entities.link(nodes[0], nodes[1], weight=v)

print('Saving file...')
with open('impeachment-partido.gdf', 'w') as f:
   entities.dump(f)
print('Saved!')
