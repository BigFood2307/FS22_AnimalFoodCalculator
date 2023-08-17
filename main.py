
import xml.etree.ElementTree as ET
from collections import Counter
from animal_types import AnimalSubType
from animal_organization import AnimalHubandry, AnimalCluster

def findSubType(list, subType, type=None):
	for idx, st in enumerate(list):
		if (type == st.type or type is None) and subType == st.subType:
			return idx
	return -1
		

baseXmlPath = "xmls/eas_animals.xml"
overrideXmlPath = "xmls/afa_eas_animalDataOverride.xml"

timeframe = 12

baseElement = ET.parse(baseXmlPath).getroot()

subtypes = []

for animalElement in baseElement.iter('animal'):
	type = animalElement.attrib['type']
	for subTypeElement in animalElement.iter('subType'):
		subtypes.append(AnimalSubType(type, subTypeElement))

overrideElement = ET.parse(overrideXmlPath).getroot()

for subTypeElement in overrideElement.iter('animalData'):
	type = subTypeElement.attrib['type']
	subType = subTypeElement.attrib['subType']
	idx = findSubType(subtypes, subType, type)
	if -1 != idx:
		subtypes[idx].override(subTypeElement)

"""
for st in subtypes:
	if len(st.outputs) > 0:
		print(st.type + "/" + st.subType + ": ")
		for key in iter(st.outputs):
			print("\t" + str(st.outputs[key].getValue(28)) + " " + key)
	else:
		print(st.type + "/" + st.subType)
"""

cowIdx = findSubType(subtypes, "COW_HOLSTEIN")
bullIdx = findSubType(subtypes, "BULL_HOLSTEIN")

cluster1 = AnimalCluster(subtypes[cowIdx], 5, 31)
cluster2 = AnimalCluster(subtypes[cowIdx], 10, 22)
cluster3 = AnimalCluster(subtypes[bullIdx], 1, 32)

pasture = AnimalHubandry()
pasture.addCluster(cluster1)
pasture.addCluster(cluster2)
pasture.addCluster(cluster3)

outputs = Counter()
inputs = Counter()

for month in range(timeframe):
	outputs.update(pasture.calcOutputs(month))
	inputs.update(pasture.calcInputs(month))

outputs = dict(outputs)
inputs = dict(inputs)

print()

print("Next Years inputs:")
for key in iter(inputs):
	print(key + ": " + str(inputs[key]))

print("Next Years outputs:")
for key in iter(outputs):
	print(key + ": " + str(outputs[key]))
