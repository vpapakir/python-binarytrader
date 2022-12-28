class econSummaryResult:

	buysOpened = 0
	buysTakeProfit = 0
	buysStopLoss = 0
	buysClosed = 0
	buyPoints = 0
	sellsOpened = 0
	sellsTakeProfit = 0
	sellsStopLoss = 0
	sellsClosed = 0
	sellPoints = 0
	totalTrades = 0
	totalWins = 0
	totalLosses1 = 0
	totalLosses2 = 0
	totalPoints = 0

	def getSummaryResults(econCalculatorObj,field):
		if field == "buyFlag":
			xCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.buyFlag) == "X":
					xCounter = xCounter + 1
			return str(xCounter)
		elif field == "buyCloseFlag1":
			tpCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.buyCloseFlag) == "TAKE PROFIT" :
					tpCounter = tpCounter + 1
			return str(tpCounter)
		elif field == "buyCloseFlag2":
			slCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.buyCloseFlag) == "STOP LOSS" :
					slCounter = slCounter + 1
			return str(slCounter)
		elif field == "buysClosed":
			return str(int(getSummaryResults(econCalculatorObj,"buyCloseFlag1"))+int(getSummaryResults(econCalculatorObj,"buyCloseFlag2")))
		elif field == "buyPoints":
			bpCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.buyCloseFlag) == "STOP LOSS":
					bpCounter = float(bpCounter) + float(items.result.buyRunningProfit)
				if str(items.result.buyCloseFlag) == "TAKE PROFIT":
					bpCounter = float(bpCounter) + float(items.result.buyRunningProfit)
			return str(bpCounter)
		elif field == "sellsOpened":
			xCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.sellFlag) == "X":
					xCounter = xCounter + 1
			return str(xCounter)
		elif field == "sellsTakeProfit":
			scfCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.sellCloseFlag) == "TAKE PROFIT":
					scfCounter = scfCounter + 1
			return str(scfCounter)
		elif field == "sellsStopLoss":
			scfCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.sellCloseFlag) == "STOP LOSS":
					scfCounter = scfCounter + 1
			return str(scfCounter)
		elif field == "sellsClosed":
			return str(int(getSummaryResults(econCalculatorObj,"sellsTakeProfit"))+int(getSummaryResults(econCalculatorObj,"sellsStopLoss")))
		elif field == "sellPoints":
			spCounter = 0
			for items in econCalculatorObj.currencyPair.cpFiles:
				if str(items.result.sellCloseFlag) == "TAKE PROFIT":
					spCounter = spCounter + float(items.result.sellCloseFlag)
				if str(items.result.sellCloseFlag) == "STOP LOSS":
					spCounter = spCounter + float(items.result.sellCloseFlag)
			return str(spCounter)
		elif field == "totalTrades":
			return str(int(getSummaryResults(econCalculatorObj,"buyFlag"))+int(getSummaryResults(econCalculatorObj,"sellsOpened")))
		elif field == "totalWins":
			return str(int(getSummaryResults(econCalculatorObj,"buyCloseFlag1"))+int(getSummaryResults(econCalculatorObj,"sellsTakeProfit")))
		elif field == "totalLosses1":
			return str(int(getSummaryResults(econCalculatorObj,"buyCloseFlag2"))+int(getSummaryResults(econCalculatorObj,"sellsStopLoss")))
		elif field == "totalLosses2":
			return str(int(getSummaryResults(econCalculatorObj,"buysClosed"))+int(getSummaryResults(econCalculatorObj,"sellsClosed")))
		elif field == "totalPoints":
			return str(int(getSummaryResults(econCalculatorObj,"buyPoints"))+int(getSummaryResults(econCalculatorObj,"sellPoints")))
		else:
			return "ERROR"	

	def __init__(self):
		pass

	def getbuysOpened(self):
		return self.buysOpened

	def setbuysOpened(self,buysOpened):
		self.buysOpened = buysOpened

	def getbuysTakeProfit(self):
		return self.buysTakeProfit

	def setbuysTakeProfit(self,buysTakeProfit):
		self.buysTakeProfit = buysTakeProfit

	def gettotalLosses1(self):
		return self.totalLosses1

	def settotalLosses1(self,totalLosses1):
		self.totalLosses1 = totalLosses1

	def gettotalLosses2(self):
		return self.totalLosses2

	def settotalLosses2(self,totalLosses2):
		self.totalLosses2 = totalLosses2

	def gettotalWins(self):
		return self.totalWins

	def settotalWins(self,totalWins):
		self.totalWins = totalWins

	def gettotalTrades(self):
		return self.totalTrades

	def settotalTrades(self,totalTrades):
		self.totalTrades = totalTrades

	def getsellPoints(self):
		return self.sellPoints

	def setsellPoints(self,sellPoints):
		self.sellPoints = sellPoints

	def getsellsClosed(self):
		return self.sellsClosed

	def setsellsClosed(self,sellsClosed):
		self.sellsClosed = sellsClosed

	def getsellsStopLoss(self):
		return self.sellsStopLoss

	def setsellsStopLoss(self,sellsStopLoss):
		self.sellsStopLoss = sellsStopLoss

	def getsellsTakeProfit(self):
		return self.sellsTakeProfit

	def setsellsTakeProfit(self,sellsTakeProfit):
		self.sellsTakeProfit = sellsTakeProfit

	def getsellsOpened(self):
		return self.sellsOpened

	def setsellsOpened(self,sellsOpened):
		self.sellsOpened = sellsOpened

	def getbuyPoints(self):
		return self.buyPoints

	def setbuyPoints(self,buyPoints):
		self.buyPoints = buyPoints

	def getbuysClosed(self):
		return self.buysClosed

	def setbuysClosed(self,buysClosed):
		self.buysClosed = buysClosed

	def getbuysStopLoss(self):
		return self.buysStopLoss

	def setbuysStopLoss(self,buysStopLoss):
		self.buysStopLoss = buysStopLoss 

	def gettotalPoints(self):
		return self.totalPoints

	def settotalPoints(self,totalPoints):
		self.totalPoints = totalPoints

