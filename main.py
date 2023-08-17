
import xml.etree.ElementTree as ET
from collections import Counter
from animal_types import AnimalSubType
from animal_organization import AnimalHubandry
import math

from utility import	findSubType

# Config start

settingsXmlPath = "xmls/script_settings.xml"

# Config end

# Read settings
settingsElement = ET.parse(settingsXmlPath).getroot()

baseXmlPath = settingsElement.find('baseXml').attrib['path']
overrideXmlPath = settingsElement.find('overrideXml').attrib['path']
placeablesXml = settingsElement.find('placeablesXml').attrib['path']

farmIds = []

for farmIdElement in settingsElement.find('farmIds').iter('farmId'):
	farmIds.append(int(farmIdElement.attrib['id']))

timeframe =  int(settingsElement.find('timeframe').attrib['months'])

ageFilter = [0, math.inf]
ageFilter[0] = int(settingsElement.find('ageFilter').attrib['min'])
ageFilter[1] = int(settingsElement.find('ageFilter').attrib['max'])

subTypeFilter = []

for subTypeElement in settingsElement.find('subTypeFilter').iter('subType'):
	subTypeFilter.append(subTypeElement.attrib['name'])

daysPerMonth =  int(settingsElement.find('daysPerMonth').attrib['days'])

# Read subtypes
baseElement = ET.parse(baseXmlPath).getroot()

subtypes = []

for animalElement in baseElement.iter('animal'):
	type = animalElement.attrib['type']
	for subTypeElement in animalElement.iter('subType'):
		subtypes.append(AnimalSubType(type, subTypeElement))

# Override subtypes
if overrideXmlPath != "":
	overrideElement = ET.parse(overrideXmlPath).getroot()

	for subTypeElement in overrideElement.iter('animalData'):
		type = subTypeElement.attrib['type']
		subType = subTypeElement.attrib['subType']
		idx = findSubType(subtypes, subType, type)
		if -1 != idx:
			subtypes[idx].override(subTypeElement)

# Read placeables
husbandries = AnimalHubandry.allFromPlaceables(placeablesXml, farmIds, subtypes)

# Compute Food
outputs = Counter()
inputs = Counter()

for month in range(timeframe):
	newIn, newOut = AnimalHubandry.calcInOutAll(husbandries, month, ageFilter, subTypeFilter)
	outputs.update(newOut)
	inputs.update(newIn)

outputs = dict(outputs)
inputs = dict(inputs)

# Output
print("Inputs:")
for key in iter(inputs):
	perDay = inputs[key]/(12*daysPerMonth)
	print(key + ": " + str(inputs[key]) + " (" + str(perDay) + ")")

print()

print("Outputs:")
for key in iter(outputs):
	perDay = outputs[key]/(12*daysPerMonth)
	print(key + ": " + str(outputs[key]) + " (" + str(perDay) + ")")

input("Press Enter to finish")