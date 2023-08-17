 
from animal_types import AnimalSubType
from collections import Counter

class AnimalCluster:
	def __init__(self, subType, count, age):
		self.subType = subType
		self.count = count
		self.age = age
	
	def calcInputs(self, extraMonths=0):
		inputs = dict()
		for key in iter(self.subType.inputs):
			inputs[key] = self.subType.inputs[key].getValue(self.age + extraMonths) * self.count
		return inputs

	def calcOutputs(self, extraMonths=0):
		outputs = dict()
		for key in iter(self.subType.outputs):
			outputs[key] = self.subType.outputs[key].getValue(self.age + extraMonths) * self.count
		return outputs


class AnimalHubandry:
	def __init__(self):
		self.clusters = []

	def addCluster(self, cluster):
		self.clusters.append(cluster)
	
	def calcInputs(self, extraMonths=0):
		inputs = Counter()
		for cluster in self.clusters:
			inputs.update(cluster.calcInputs(extraMonths))
		return dict(inputs)
	
	def calcOutputs(self, extraMonths=0):
		outputs = Counter()
		for cluster in self.clusters:
			outputs.update(cluster.calcOutputs(extraMonths))
		return dict(outputs)