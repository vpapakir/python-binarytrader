class InputDirScanner:
	path = "./input/"

	def __init__(self,path):
		self.path = path

	def scan(self):
		terminateLoop = 0
		while terminateLoop == 0:
			print "Scanning..."
