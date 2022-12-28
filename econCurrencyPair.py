class econCurrencyPair:
	pairMember1 = ""
	pairMember2 = ""
	path = ""
	cpFiles = []

	def __init__(self,pairMember1,pairMember2,path,cpFiles):
		self.pairMember1 = pairMember1
		self.pairMember2 = pairMember2
		self.path = path
		self.cpFiles = cpFiles

	def getCpFiles(self):
		return self.cpFiles

	def setCpFiles(self,cpFiles):
		self.cpFiles = cpFiles
