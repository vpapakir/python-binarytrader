class Input:
	case=0
	weekendTimeout=300
	maxSpread=14
	activityCriterion=0.0008
	invertEMA=-1
	buyRSI=0
	buyEMADist=0
	sellRSI=70
	sellEMADist=0
	takeProfit=0
	stopLoss=0
	calculateDetailed = 1

	def __init__(self,row):
		self.data = []
		self.case = row[0]
		self.weekendTimeout = row[1]
		self.maxSpread = row[2]
		self.activityCriterion = row[3]
		self.invertEMA = row[4]
		self.buyRSI = row[5]
		self.buyEMADist = row[6]
		self.sellRSI = row[7]
		self.sellEMADist = row[8]
		self.takeProfit = row[9]
		self.stopLoss = row[10]
		self.calculateDetailed = row[11]
