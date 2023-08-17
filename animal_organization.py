 
from animal_types import AnimalSubType
from collections import Counter
import xml.etree.ElementTree as ET
from utility import	findSubType
import math

class AnimalCluster:
	def __init__(self, subType, count, age):
		self.subType = subType
		self.count = count
		self.age = age
	
	def calcInputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=None):
		inputs = dict()
		specifiedAge = self.age + extraMonths
		if specifiedAge < ageFilter[0] or specifiedAge > ageFilter[1]:
			return inputs
		if subTypeFilter is not None:
			if not self.subType.subType in subTypeFilter:
				return inputs
		for key in iter(self.subType.inputs):
			inputs[key] = self.subType.inputs[key].getValue(specifiedAge) * self.count
		return inputs

	def calcOutputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=None):
		outputs = dict()
		specifiedAge = self.age + extraMonths
		if specifiedAge < ageFilter[0] or specifiedAge > ageFilter[1]:
			return outputs
		if subTypeFilter is not None:
			if not self.subType.subType in subTypeFilter:
				return outputs
		for key in iter(self.subType.outputs):
			outputs[key] = self.subType.outputs[key].getValue(specifiedAge) * self.count
		return outputs
	
	@staticmethod
	def fromXml(element, subtypes):
		subType = findSubType(subtypes, element.attrib['subType'])
		count = int(element.attrib['numAnimals'])
		age = int(element.attrib['age'])
		return AnimalCluster(subtypes[subType], count, age)



class AnimalHubandry:
	def __init__(self):
		self.clusters = []

	def addCluster(self, cluster):
		self.clusters.append(cluster)
	
	def calcInputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=None):
		inputs = Counter()
		for cluster in self.clusters:
			inputs.update(cluster.calcInputs(extraMonths, ageFilter, subTypeFilter))
		return dict(inputs)
	
	def calcOutputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=None):
		outputs = Counter()
		for cluster in self.clusters:
			outputs.update(cluster.calcOutputs(extraMonths, ageFilter, subTypeFilter))
		return dict(outputs)
	
	@staticmethod
	def calcInOutAll(husbandries, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=None):		
		outputs = Counter()
		inputs = Counter()
		for husbandry in husbandries:
			outputs.update(husbandry.calcOutputs(extraMonths, ageFilter, subTypeFilter))
			inputs.update(husbandry.calcInputs(extraMonths, ageFilter, subTypeFilter))
		return dict(inputs), dict(outputs)

	
	@staticmethod
	def fromXml(element, subtypes):
		husbandry = AnimalHubandry()
		for cluster in element.iter('animal'):
			husbandry.addCluster(AnimalCluster.fromXml(cluster, subtypes))
		return husbandry
	
	@staticmethod
	def allFromPlaceables(xmlPath, farmIds, subtypes):
		husbandries = []
		placeablesElement = ET.parse(xmlPath).getroot()
		for placeable in placeablesElement.iter('placeable'):
			husbandryElement = placeable.find('husbandryAnimals')
			if husbandryElement is not None:
				farmId = int(placeable.attrib['farmId'])
				if farmId in farmIds:
					clustersElement = husbandryElement.find('clusters')
					if clustersElement is not None:
						husbandry = AnimalHubandry.fromXml(clustersElement, subtypes)
						husbandries.append(husbandry)
		return husbandries

