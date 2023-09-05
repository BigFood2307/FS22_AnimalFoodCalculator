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
easSettingsXmlPath = settingsElement.find('easSettingsXml').attrib['path']
easUsed =  easSettingsXmlPath != ""

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

# Read eas settings, if used

typeToLactationValues = None
typeToFoodValues = None

if easUsed:
	easSettingsElement = ET.parse(easSettingsXmlPath).getroot().find('Settings')

	typeToLactationSetting = dict()
	typeToLactationValues = dict()

	typeToLactationSetting["COW"] = "CowLactation"
	typeToLactationSetting["SHEEP"] = "GoatLactation"

	typeToFoodSetting = dict()
	typeToFoodValues = dict()
		
	typeToFoodSetting["PIG"] = "PigFoodFactor"
	typeToFoodSetting["COW"] = "CowFoodFactor"
	typeToFoodSetting["HORSE"] = "HorseFoodFactor"
	typeToFoodSetting["SHEEP"] = "SheepFoodFactor"
	typeToFoodSetting["CHICKEN"] = "ChickenFoodFactor"

	for type in typeToLactationSetting.keys():
		typeToLactationValues[type] = easSettingsElement.attrib[typeToLactationSetting[type]].split(',')
		typeToLactationValues[type] = [float(string) for string in typeToLactationValues[type]]

	for type in typeToFoodSetting.keys():
		typeToFoodValues[type] = easSettingsElement.attrib[typeToFoodSetting[type]].split(',')
		typeToFoodValues[type] = [float(string) for string in typeToFoodValues[type]]

# Read placeables
husbandries = AnimalHusbandry.allFromPlaceables(placeablesXml, farmIds, subtypes, easUsed, typeToLactationValues, typeToFoodValues)


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