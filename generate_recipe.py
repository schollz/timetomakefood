import yaml
from pint import UnitRegistry
import sys

ureg = UnitRegistry()

def start_print_dict(item,fullDict,printOut,stats):
  if printOut:
    return print_dict(fullDict[item],'',fullDict)
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
          else:
            # Add it to the basic ingredient list
            try:
              if e['name'] in stats['ingredients']:
                stats['ingredients'][e['name']] = stats['ingredients'][e['name']] + (float(e['amount'].split()[0])*ureg.parse_expression(e['amount'].split()[1]))
              else:
                stats['ingredients'][e['name']] =(float(e['amount'].split()[0])*ureg.parse_expression(e['amount'].split()[1]))
            except:
              stats['ingredients'][e['name']] = e['amount']

        string = string + "\n"
    if 'mix' == key:
      string = string + "Mix them together\n"
      print value.keys()
      if 'time' in value.keys():
        print value['time']
        stats['time'] = stats['time'] + (float(value['time'].split()[0])*ureg.parse_expression(value['time'].split()[1]))
      else:
        stats['time'] = stats['time'] + 2*ureg.minute
    if 'cook' == key:
      string = string + value['type'] + " at " + value['heat'] + " for " + value['time'] + "\n"
      stats['time'] = stats['time'] + (float(value['time'].split()[0])*ureg.parse_expression(value['time'].split()[1]))
    if 'set' == key:
      if 'type' in value:
        string = string + value['type'] + " "
      else:
        string = string + "set" + " "      
      if 'time' in value:
        string = string + "for " + value['time'] + "\n"
        stats['time'] = stats['time'] + (float(value['time'].split()[0])*ureg.parse_expression(value['time'].split()[1]))
      else:
        string = string + "\n"    
    if 'cut' == key:
      string = string + value['type'] + " into " + value['pieces']  + "\n"
      if 'time' in value:
        stats['time'] = stats['time'] + (float(value['time'].split()[0])*ureg.parse_expression(value['time'].split()[1]))
      else:
        stats['time'] = stats['time'] + 3*ureg.minute
  return string
    
      
stream = open('recipes.yaml','r')
data = yaml.load(stream, yaml.SafeLoader)
stats = {}
stats['time']=0*ureg.minute
try:
  food = sys.argv[1]
except:
  food = "none"
stats['ingredients']={}

if food in data.keys():
  stats['directions'] = start_print_dict(food,data,True,stats)
  if stats['time'].magnitude > 100:
    stats['time'] = stats['time'].to(ureg.hour)

  print "How to make a " + food + " from scratch"
  print "------------------------------------------\n"

  print "Time needed: ",
  print stats['time']

  print "\nBasic ingredient list:"
  for e in stats['ingredients']:
    print stats['ingredients'][e],
    print " " + e 
  print "\n"

  print "Directions: "
  print stats['directions']
else:
  print food + " not in recipe database"
  print "\nAvailable recipes\n--------------------"
  for e in sorted(data.keys()):
    print " - " + e
  print "\n"
