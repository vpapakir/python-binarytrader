class econResult:

	timeOut = ""
	spreadFlag = ""
	activityFlag = ""
	buyRSI = ""
	buyEMADist = ""
	buyFlag = ""
	buyPrice = ""
	buyRunningProfit = ""
	buyCloseFlag = ""
	sellRSI = ""
	sellEMADist = ""
	sellFlag = ""
	sellPrice = ""
	sellRunningProfit = ""
	sellCloseFlag = ""

	def __init__(self):
		self.data = []

	def getTimeOut(self):
		return self.timeOut

	def getSpreadFlag(self):
		return self.spreadFlag

	def getActivityFlag(self):
		return self.activityFlag

	def getBuyRSI(self):
		return self.buyRSI

	def getBuyEMADist(self):
		return self.buyEMADist

	def getBuyFlag(self):
		return self.buyFlag

	def getBuyPrice(self):
		return self.buyPrice

	def getBuyRunningProfit(self):
		return self.buyRunningProfit

	def getBuyCloseFlag(self):
		return self.buyCloseFlag

	def getSellRSI(self):
		return self.sellRSI

	def getSellEMADist(self):
		return self.sellEMADist

	def getSellFlag(self):
		return self.sellFlag

	def getSellPrice(self):
		return self.sellPrice

	def getSellRunningProfit(self):
		return self.sellRunningProfit

	def getSellCloseFlag(self):
		return self.sellCloseFlag

	def setTimeOut(self,timeOut):
		self.timeOut = timeOut

	def setSpreadFlag(self,spreadFlag):
		self.spreadFlag = spreadFlag

	def setActivityFlag(self,activityFlag):
		self.activityFlag = activityFlag

	def setBuyRSI(self,buyRSI):
		self.buyRSI = buyRSI

	def setBuyEMADist(self,buyEMADist):
		self.buyEMADist = buyEMADist

	def setBuyFlag(self,buyFlag):
		self.buyFlag = buyFlag

	def setBuyPrice(self,buyPrice):
		self.buyPrice = buyPrice

	def setBuyRunningProfit(self,buyRunningProfit):
		self.buyRunningProfit = buyRunningProfit

	def setBuyCloseFlag(self,buyCloseFlag):
		self.buyCloseFlag = buyCloseFlag

	def setSellRSI(self,sellRSI):
		self.sellRSI = sellRSI

	def setSellEMADist(self,sellEMADist):
		self.sellEMADist = sellEMADist

	def setSellFlag(self,sellFlag):
		self.sellFlag = sellFlag

	def setSellPrice(self,sellPrice):
		self.sellPrice = sellPrice

	def setSellRunningProfit(self,sellRunningProfit):
		self.sellRunningProfit = sellRunningProfit

	def setSellCloseFlag(self,sellCloseFlag):
		self.sellCloseFlag = sellCloseFlag
