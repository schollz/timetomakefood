import yaml
from pint import UnitRegistry

ureg = UnitRegistry()

def start_print_dict(item,fullDict,printOut,stats):
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
						string = start_print_dict(e['name'],fullDict,False,stats) + "\n" + string
				string = string + "\n"
		if 'mix' == key:
			string = string + "Mix them together\n"
			stats['time'] = stats['time'] + 2*ureg.minute
		if 'cook' == key:
			string = string + value['type'] + " at " + value['heat'] + " for " + value['time'] + "\n"
			stats['time'] = stats['time'] + (int(value['time'].split()[0])*ureg.parse_expression(value['time'].split()[1]))
		if 'set' == key:
			string = string + "Set for " + value['time'] + "\n"
			stats['time'] = stats['time'] + (int(value['time'].split()[0])*ureg.parse_expression(value['time'].split()[1]))
		if 'cut' == key:
			string = string + value['type'] + " into " + value['pieces']  + "\n"
			stats['time'] = stats['time'] + 3*ureg.minute
	return string
		
			
stream = open('recipes.yaml','r')
data = yaml.load(stream, yaml.SafeLoader)
stats = {}
stats['time']=0*ureg.minute
print start_print_dict('grilled cheese sandwich',data,True,stats)
print stats

		
