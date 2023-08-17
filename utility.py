def findSubType(list, subType, type=None):
	for idx, st in enumerate(list):
		if (type == st.type or type is None) and subType == st.subType:
			return idx
	return -1		