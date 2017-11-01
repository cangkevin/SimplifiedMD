import json

data2 = []

with open('data2.json') as js1:
	js_data = js1.read()
	a = json.loads(js_data)
	for line in a:
		data2.append(line)
		
data3 = []
with open('data3.json') as js2:
	js_data = js2.read()
	a = json.loads(js_data)
	for line in a:
		data3.append(line)
		
for line in data3:
	if line not in data2:
		print line
		print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"