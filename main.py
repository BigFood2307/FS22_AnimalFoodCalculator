
import xml.etree.ElementTree as ET
from collections import Counter
from animal_types import AnimalSubType
from animal_organization import AnimalHubandry, AnimalCluster

from utility import	findSubType

# Config start

baseXmlPath = "xmls/eas_animals.xml"
overrideXmlPath = "xmls/afa_eas_animalDataOverride.xml" # None if no M+ is used
placeablesXml = "xmls/sample_placeables.xml"

farmIds = [0, 1]

timeframe = 12

ageFilter = [8, 1000]
subTypeFilter = ["COW_HOLSTEIN", "BULL_HOLSTEIN"]

daysPerMonth = 4

# Config end

baseElement = ET.parse(baseXmlPath).getroot()

subtypes = []

for animalElement in baseElement.iter('animal'):
	type = animalElement.attrib['type']
	for subTypeElement in animalElement.iter('subType'):
		subtypes.append(AnimalSubType(type, subTypeElement))

if overrideXmlPath is not None:
	overrideElement = ET.parse(overrideXmlPath).getroot()

	for subTypeElement in overrideElement.iter('animalData'):
		type = subTypeElement.attrib['type']
		subType = subTypeElement.attrib['subType']
		idx = findSubType(subtypes, subType, type)
		if -1 != idx:
			subtypes[idx].override(subTypeElement)

husbandries = AnimalHubandry.allFromPlaceables(placeablesXml, farmIds, subtypes)

outputs = Counter()
inputs = Counter()

for month in range(timeframe):
	newIn, newOut = AnimalHubandry.calcInOutAll(husbandries, month, ageFilter, subTypeFilter)
	outputs.update(newOut)
	inputs.update(newIn)

outputs = dict(outputs)
inputs = dict(inputs)

print("Inputs:")
for key in iter(inputs):
	perDay = inputs[key]/(12*daysPerMonth)
	print(key + ": " + str(inputs[key]) + " (" + str(perDay) + ")")

print()

print("Outputs:")
for key in iter(outputs):
	perDay = outputs[key]/(12*daysPerMonth)
	print(key + ": " + str(outputs[key]) + " (" + str(perDay) + ")")
