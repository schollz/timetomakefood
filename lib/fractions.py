import math
from humanize import intcomma

def get_fraction(f):
	"""
	Rounds fraction to nearest 1/4th
	"""
	fracs = (int(round(f*4))/4).as_integer_ratio()
	firstNum = math.floor(fracs[0]/fracs[1])
	secondNum = fracs[0] % fracs[1]
	thirdNum = fracs[1]
	if firstNum == 0:
		if secondNum == 0:
			return "{}".format(thirdNum)
		else:
			return "{}/{}".format(secondNum,thirdNum)
	elif secondNum > 0 :
		return "{} {}/{}".format(intcomma(firstNum),secondNum,thirdNum)
	else:
		return firstNum
