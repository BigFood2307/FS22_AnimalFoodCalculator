from linear_table import LinearTable
import xml.etree.ElementTree as ET

class AnimalSubType:

	def __init__(self, type, element):
		self.type = type
		self.subType = element.attrib['subType']

		reproduction = element.find('reproduction')
		self.durationMonth = None
		self.minReproductionAge = None
		if "durationMonth" in reproduction.attrib.keys():
			self.durationMonth = int(reproduction.attrib['durationMonth'])
			self.minReproductionAge = int(reproduction.attrib['minAgeMonth'])

		inputElement = element.find('input')
		self.inputs = dict()
		for inputType in inputElement:
			self.inputs[inputType.tag.lower()] = LinearTable(inputType)

		outputElement = element.find('output')
		self.outputs = dict()
		for outputType in outputElement:
			self.outputs[outputType.tag.lower()] = LinearTable(outputType)
	
	def override(self, element):
		inputsElement = element.find('inputs')
		overrideType = inputsElement.attrib['overrideType']

		if overrideType == "replace":
			self.inputs = dict()

		for inputType in inputsElement.iter('input'):
			self.inputs[inputType.attrib['type'].lower()] = LinearTable(inputType)

		outputsElement = element.find('outputs')
		if outputsElement:
			overrideType = outputsElement.attrib['overrideType']

			if overrideType == "replace":
				self.outputs = dict()

			for outputType in outputsElement.iter('output'):
				self.outputs[outputType.attrib['type'].lower()] = LinearTable(outputType)

