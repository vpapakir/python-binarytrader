import csv
import calendar
import time
import atexit
import econInput
import multiprocessing
#import econCalc
#import econInputDirScanner
import sys
import logging
import os
from threading import Thread
from time import sleep

OUTPUT_LOG="./data/econ.log"
logging.basicConfig(filename=OUTPUT_LOG,level=logging.INFO)

# Process input

def split(filehandler, delimiter=',', row_limit=1000, output_name_template='./input/input_%s.csv', output_path='.', keep_headers=True):
	inputList = []
	reader = csv.reader(filehandler, delimiter=delimiter)
	current_piece = 1
	current_out_path = os.path.join(output_path,output_name_template % current_piece)
	current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
	inputList.append(current_out_path)
	current_limit = row_limit
	if keep_headers:
		headers = reader.next()
		current_out_writer.writerow(headers)
	for i, row in enumerate(reader):
		if i + 1 > current_limit:
			current_piece += 1
			current_limit = row_limit * current_piece
			current_out_path = os.path.join(output_path,output_name_template % current_piece)
			current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
			if keep_headers:
				current_out_writer.writerow(headers)
				inputList.append(current_out_path)
		current_out_writer.writerow(row)
	return inputList

def exit_handler():
	logging.info("["+str(calendar.timegm(time.gmtime()))+"] Exiting normally...")

def main(argv):
	inputObjArray = []
	inputDirScannerObj = econInputDirScanner.InputDirScanner("./input/")
	inputDirScanThread = Thread(target=inputDirScannerObj.scan,args=())
	with open(argv, 'rb') as csvfile:
		csvreaderObj = csv.reader(csvfile,delimiter=',')
		for row in csvreaderObj:
			row.append(sys.argv[3])
			inputObj = econInput.Input(row)
			inputObjArray.append(inputObj)
			try:
				val = int(inputObj.case)
				logging.info("["+str(calendar.timegm(time.gmtime()))+"] Starting calculation Case: " + str(inputObj.case) + " sellEMADist: " + str(inputObj.sellEMADist))
				calculationThread = Thread(target=econCalc.econCalculation,args=(inputObj, ))
				calculationThread.start()
				calculationThread.join()
			except ValueError:
	   			logging.info("["+str(calendar.timegm(time.gmtime()))+"] Ignoring input file header")

atexit.register(exit_handler)

if __name__ == '__main__':
	#logging.info("["+str(calendar.timegm(time.gmtime()))+"] Executing calculation with " + sys.argv[0] + " and " + sys.argv[1] + " and " + sys.argv[2] + " and " + sys.argv[3])
	count = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=count)
	inList = split(open(sys.argv[1],'r'),",",round((int(sys.argv[2])-1)/count))
	#print pool.map(main, inList)
