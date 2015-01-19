import yaml

def start_print_dict(item,fullDict,printOut):
	if printOut:
		return 'To make ' + fullDict[item]['amount'] + ' ' + item + ':\n\n' + print_dict(fullDict[item],'',fullDict)
	else:
		return print_dict(fullDict[item],'',fullDict)

def print_dict(dictionary, string, fullDict):
	for key, value in dictionary.iteritems():
		if isinstance(value, dict):
			string = print_dict(value,  string, fullDict)
		else:
			if "ingredient" in key:
				num = 0
				string = string + "Take"
				for e in dictionary[key]:
					if num > 0:
						string = string + "and"
					string = string + " " + e['amount'] + ' ' + e['name'] + " "
					num = num + 1
					if e['name'] in fullDict.keys():
						string = start_print_dict(e['name'],fullDict,False) + "\n" + string
				string = string + "\n"
		if 'mix' == key:
			string = string + "Mix them together\n"
		if 'cook' == key:
			string = string + value['type'] + " at " + value['heat'] + " for " + value['time'] + "\n"
		if 'set' == key:
			string = string + "Set for " + value['time'] + "\n"
		if 'cut' == key:
			string = string + value['type'] + " into " + value['pieces']  + "\n"
	return string
		
			
stream = open('recipes.yaml','r')
data = yaml.load(stream, yaml.SafeLoader)
print start_print_dict('grilled cheese sandwich',data,True)

		
