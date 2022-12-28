from econResult import econResult

class econCurrencyPairEntry:
	timeUTC = ""
	high1 = 0
	low1 = 0
	bid1 = 0
	ask1 = 0
	volume1 = 0
	spread = 0
	high2 = 0
	low2 = 0
	bid2 = 0
	ask2 = 0
	volume2 = 0
	atr = 0
	rsi = 0
	emadIst = 0
	fileid = 0
	result = ""

	def __init__(self,entry,fileid):
		self.timeUTC = str(entry[0])
		self.high1 = str(entry[1])
		self.low1 = str(entry[2])
		self.bid1 = str(entry[3])
		self.ask1 = str(entry[4])
		self.volume1 = str(entry[5])
		self.spread = str(entry[6])
		self.high2 = str(entry[7])
		self.low2 = str(entry[8])
		self.bid2 = str(entry[9])
		self.ask2 = str(entry[10])
		self.volume2 = str(entry[11])
		self.atr = str(entry[12])
		self.rsi = str(entry[13])
		self.emadIst = str(entry[14])
		self.fileid = str(fileid)
		self.result = econResult()

	def getResult(self):
		return self.result

	def setResult(self,result):
		self.result = result
