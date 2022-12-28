import datetime
import gzip
import shutil

class Archiver:
	archiveType='input'
	archivePath='./input/'
	archiveDestination='./archive/input/'
	timeStamp=''

	def __init__(self,archiveType,archivePath,archiveDestination,timeStamp):
		self.archiveType=archiveType
		self.archivePath=archivePath
		self.archiveDestination=archiveDestination
		self.timeStamp=timeStamp

	def archive():
		with open('file.txt', 'rb') as f_in, gzip.open('file.txt.gz', 'wb') as f_out:
			print "Archiving..."
			shutil.copyfileobj(f_in, f_out)
