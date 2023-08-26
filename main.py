import tkinter as tk
import xml.etree.ElementTree as ET
from collections import Counter
from animal_types import AnimalSubType
from animal_organization import AnimalHusbandry
import math

from gui.animal_food_frame import AnimalFoodFrame

from utility import	findSubType, calcInOut

# Config start

width=1200
height=800

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

daysPerMonth = int(settingsElement.find('daysPerMonth').attrib['days'])

useGui = settingsElement.find('gui').attrib['useBasicGui'] == "True"

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
husbandries = AnimalHusbandry.allFromPlaceables(placeablesXml, farmIds, subtypes)

if not useGui:
	# Compute Food

	inputs, outputs = calcInOut(husbandries, ageFilter, subTypeFilter, timeframe)

	# Output

	print("Inputs:")
	for key in iter(inputs):
		perDay = inputs[key]/(timeframe*daysPerMonth)
		print(key + ": " + str(inputs[key]) + " (" + str(perDay) + ")")

	print()

	print("Outputs:")
	for key in iter(outputs):
		perDay = outputs[key]/(timeframe*daysPerMonth)
		print(key + ": " + str(outputs[key]) + " (" + str(perDay) + ")")

	input("Press Enter to finish")

else:

	tkRoot = tk.Tk()
	tkRoot.geometry(str(width) + "x" + str(height))
	tkRoot.resizable(False, False)
	tkRoot.title("FS22 Animal Food Calculator")
	myapp = AnimalFoodFrame(tkRoot, height, subtypes, husbandries, daysPerMonth, timeframe, ageFilter, subTypeFilter)

	tkRoot.mainloop()