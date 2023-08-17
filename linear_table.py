import xml.etree.ElementTree as ET

class LinearTable:

	def __init__(self):
		self.table = dict()
	
	def __init__(self, element):
		self.table = dict()
		for line in element.iter('key'):
			key = int(line.attrib['ageMonth'])
			value = int(line.attrib['value'])
			self.table[key] = value


	def getValue(self, age):
		lastKey = 0
		lastValue = 0
		for key, value in self.table.items():
			if key > age:
				ratio = (age - lastKey)/(key - lastKey)
				return lastValue + (value - lastValue)*ratio
			lastKey = key
			lastValue = value
		return lastValue
