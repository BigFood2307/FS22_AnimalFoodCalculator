 
from animal_types import AnimalSubType
from collections import Counter
import xml.etree.ElementTree as ET
from utility import	findSubType, nameFromPath
import math

class AnimalCluster:
	def __init__(self, subType, count, age, reproduction, easUsed):
		self.subType = subType
		self.count = count
		self.age = age
		self.reproduction = reproduction
		self.easUsed = easUsed
	
	def calcInputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=[]):
		inputs = dict()
		specifiedAge = self.age + extraMonths
		if specifiedAge < ageFilter[0] or specifiedAge > ageFilter[1]:
			return inputs
		if subTypeFilter != []:
			if not self.subType.subType in subTypeFilter:
				return inputs
		for key in iter(self.subType.inputs):
			inputs[key] = self.subType.inputs[key].getValue(specifiedAge) * self.count			

			# special case food for EAS:
			if key == "food" and (self.easUsed and self.foodFactors is not None):
				factor = 1
				if self.subType.minReproductionAge is not None:
					actualReproduction = self.reproduction
					actualMonthsSinceLastBirth = self.monthsSinceLastBirth
					if self.subType.minReproductionAge is not None and specifiedAge > self.subType.minReproductionAge:
						reproductiveMonths = extraMonths - (self.subType.minReproductionAge - self.age)
						# assume automatic insemination
						actualReproduction = actualReproduction + (100/self.subType.durationMonth)*reproductiveMonths
						actualHadABirth = self.hadABirth or actualReproduction >= 100
						actualReproduction = actualReproduction%100
						actualMonthsSinceLastBirth = (actualMonthsSinceLastBirth + reproductiveMonths)%self.subType.durationMonth

						if actualHadABirth and actualMonthsSinceLastBirth < len(self.foodFactors):
							factor = self.foodFactors[actualMonthsSinceLastBirth]				
				inputs[key] = inputs[key]*factor
		return inputs

	def calcOutputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=[]):
		outputs = dict()
		specifiedAge = self.age + extraMonths
		if specifiedAge < ageFilter[0] or specifiedAge > ageFilter[1]:
			return outputs
		if subTypeFilter != []:
			if not self.subType.subType in subTypeFilter:
				return outputs
		for key in iter(self.subType.outputs):
			outputs[key] = self.subType.outputs[key].getValue(specifiedAge) * self.count

			# special case milk for EAS:
			if key == "milk" and (self.easUsed and self.lactationFactors is not None):
				factor = 0
				actualReproduction = self.reproduction
				actualMonthsSinceLastBirth = self.monthsSinceLastBirth
				actualHadABirth = self.hadABirth
				if self.subType.minReproductionAge is not None and specifiedAge > self.subType.minReproductionAge:
					reproductiveMonths = extraMonths - (self.subType.minReproductionAge - self.age)
					# assume automatic insemination
					actualReproduction = actualReproduction + (100/self.subType.durationMonth)*reproductiveMonths
					actualHadABirth = actualHadABirth or actualReproduction >= 100
					actualReproduction = actualReproduction%100
					actualMonthsSinceLastBirth = (actualMonthsSinceLastBirth + reproductiveMonths)%self.subType.durationMonth
				if actualReproduction < 80 and actualHadABirth:
					if actualMonthsSinceLastBirth < len(self.lactationFactors):
						factor = self.lactationFactors[actualMonthsSinceLastBirth]				
				outputs[key] = outputs[key]*factor
		return outputs
	
	@staticmethod
	def fromXml(element, subtypes, easUsed, lactationFactors=None, foodFactors=None):
		subType = subtypes[findSubType(subtypes, element.attrib['subType'])]

		count = int(element.attrib['numAnimals'])
		age = int(element.attrib['age'])
		reproduction = int(element.attrib['reproduction'])

		cluster = AnimalCluster(subType, count, age, reproduction, easUsed)

		if easUsed:
			cluster.monthsSinceLastBirth = int(element.attrib['monthsSinceLastBirth'])
			cluster.hadABirth = element.attrib['hadABirth'] == "true"

			if subType.type in lactationFactors.keys():
				cluster.lactationFactors = lactationFactors[subType.type]
			else:
				cluster.lactationFactors = None
				
			if subType.type in foodFactors.keys():
				cluster.foodFactors = foodFactors[subType.type]
			else:
				cluster.foodFactors = None

		return cluster



class AnimalHusbandry:
	def __init__(self, name):
		self.clusters = []
		self.name = name
		self.enabled = True

	def addCluster(self, cluster):
		self.clusters.append(cluster)
	
	def calcInputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=[]):
		inputs = Counter()
		if not self.enabled:
			return inputs
		for cluster in self.clusters:
			inputs.update(cluster.calcInputs(extraMonths, ageFilter, subTypeFilter))
		return dict(inputs)
	
	def calcOutputs(self, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=[]):
		outputs = Counter()
		if not self.enabled:
			return outputs
		for cluster in self.clusters:
			outputs.update(cluster.calcOutputs(extraMonths, ageFilter, subTypeFilter))
		return dict(outputs)
	
	@staticmethod
	def calcInOutAll(husbandries, extraMonths=0, ageFilter=[0, math.inf], subTypeFilter=[]):		
		outputs = Counter()
		inputs = Counter()
		for husbandry in husbandries:
			outputs.update(husbandry.calcOutputs(extraMonths, ageFilter, subTypeFilter))
			inputs.update(husbandry.calcInputs(extraMonths, ageFilter, subTypeFilter))
		return dict(inputs), dict(outputs)

	
	@staticmethod
	def fromXml(element, subtypes, name, easUsed, lactationFactors=None, foodFactors=None):
		husbandry = AnimalHusbandry(name)
		if element is not None:
			for cluster in element.iter('animal'):
				husbandry.addCluster(AnimalCluster.fromXml(cluster, subtypes, easUsed, lactationFactors, foodFactors))
		return husbandry
	
	@staticmethod
	def allFromPlaceables(xmlPath, farmIds, subtypes, easUsed, lactationFactors=None, foodFactors=None):
		husbandries = []
		placeablesElement = ET.parse(xmlPath).getroot()
		for placeable in placeablesElement.iter('placeable'):
			husbandryElement = placeable.find('husbandryAnimals')
			if husbandryElement is not None:
				husbandryName = nameFromPath(placeable.attrib['filename'])
				renamed = 'name' in placeable.attrib.keys()
				if renamed:
					husbandryName = placeable.attrib['name']
				farmId = int(placeable.attrib['farmId'])
				if farmId in farmIds:
					clustersElement = husbandryElement.find('clusters')
					if clustersElement is not None:
						husbandry = AnimalHusbandry.fromXml(clustersElement, subtypes, husbandryName, easUsed, lactationFactors, foodFactors)
						husbandries.append(husbandry)
		return husbandries

