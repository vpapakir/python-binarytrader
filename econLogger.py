class econLogger:
	logFile = "./log/econ/log"
	timeStamp = ""
	logMessage = ""

	def __init__(self):
		self.data = []

	def getLogFile(self):
		return self.logFile

	def setLogFile(self,logFile):
		self.logFile = logFile

	def getTimeStamp(self):
		return self.timeStamp

	def setTimeStamp(self,timeStamp):
		self.timeStamp = timeStamp

	def setLogMessage(self,message):
		pass #TODO
