class econDetailedResultEntry:
	tradeNo = "X"
	openDateTime = "X"
	openPrice = "X"
	closeDateTime = "X"
	closePrice = "X"
	duration = "X"
	typeIndicator = "X"
	points = "X"
	closeMethod = "X"

	def __init__(self, tradeNo, openDateTime, openPrice, closeDateTime, closePrice, duration, typeIndicator, points, closeMethod):
		self.tradeNo = tradeNo
		self.openDateTime = openDateTime
		self.openPrice = openPrice
		self.closeDateTime = closeDateTime
		self.closePrice = closePrice
		self.duration = duration
		self.typeIndicator = typeIndicator
		self.points = points
		self.closeMethod = closeMethod
