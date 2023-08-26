
from collections import Counter

def findSubType(list, subType, type=None):
	for idx, st in enumerate(list):
		if (type == st.type or type is None) and subType == st.subType:
			return idx
	return -1		

def nameFromPath(path):
	file = path.split('/')[-1]
	return file.split('.')[0]

def calcInOut(husbandries, ageFilter, subTypeFilter, timeframe):	
	from animal_organization import AnimalHusbandry
	outputs = Counter()
	inputs = Counter()

	for month in range(timeframe):
		newIn, newOut = AnimalHusbandry.calcInOutAll(husbandries, month, ageFilter, subTypeFilter)
		outputs.update(newOut)
		inputs.update(newIn)

	outputs = dict(outputs)
	inputs = dict(inputs)

	return inputs, outputs