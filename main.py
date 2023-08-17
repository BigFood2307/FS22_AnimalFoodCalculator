
import xml.etree.ElementTree as ET
from collections import Counter
from animal_types import AnimalSubType
from animal_organization import AnimalHubandry, AnimalCluster

from utility import	findSubType

baseXmlPath = "xmls/eas_animals.xml"
overrideXmlPath = "xmls/afa_eas_animalDataOverride.xml"
placeablesXml = "xmls/sample_placeables.xml"

farmIds = [1]

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

husbandries = AnimalHubandry.allFromPlaceables(placeablesXml, farmIds, subtypes)

outputs = Counter()
inputs = Counter()

for month in range(timeframe):
	newIn, newOut = AnimalHubandry.calcInOutAll(husbandries, month, [8, 1000], ["COW_HOLSTEIN"])
	outputs.update(newOut)
	inputs.update(newIn)

outputs = dict(outputs)
inputs = dict(inputs)

print("Next Years inputs:")
for key in iter(inputs):
	print(key + ": " + str(inputs[key]))

print("Next Years outputs:")
for key in iter(outputs):
	print(key + ": " + str(outputs[key]))
