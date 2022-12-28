import threading
import csv
import logging
import os
import calendar
import time
from datetime import datetime, date
from time import sleep
from threading import Thread
from econCurrencyPair import econCurrencyPair
from econSummaryResult import econSummaryResult
from econCurrencyPairEntry import econCurrencyPairEntry
from econCalculator import econCalculator
from econDetailedResultEntry import econDetailedResultEntry

logging.basicConfig(filename='./econ.log',level=logging.INFO)

def groupByPrefix(strings,pfix):
	stringsByPrefix = {}
	for string in strings:
		prefix, suffix = map(str.strip, string.split(pfix, 1))
		group = stringsByPrefix.setdefault(prefix, [])
		group.append(suffix)
	return stringsByPrefix

def spawnCurrencyPairThread(inputArr,pairMember1,pairMember2,path,fileids):
	currencyPairEntryArr = []
	logging.info("["+str(calendar.timegm(time.gmtime()))+"] Case " + inputArr.case + " Starting CurrencyPair thread: " + pairMember1 + "//"  + pairMember2 + " in " + str(path) + " => " + str(path) + " @thread: " + threading.current_thread().name)
	for fileid in fileids:
		#logging.info("["+str(calendar.timegm(time.gmtime()))+"] Case " + inputArr.case + " opening currency file: " + pairMember1 + "//"  + pairMember2 + " in " + str(path) + " => " + str(fileid) + " @thread: " + threading.current_thread().name)
		with open(path + pairMember1 + pairMember2 + "-" + fileid, 'rb') as csvfile:
			csvreaderObj = csv.reader(csvfile,delimiter=',')
			for row in csvreaderObj:
				try:
					val = float(row[1])
					row[14] = float(row[14])
					currencyPairEntryObj = econCurrencyPairEntry(row,fileid)
					currencyPairEntryArr.append(currencyPairEntryObj)
					#logging.info("["+str(calendar.timegm(time.gmtime()))+"] Case " + inputArr.case + " checking last currencyPairEntryArr entry: " + str(currencyPairEntryArr[-1].timeUTC) + " " + str(currencyPairEntryArr[-1].emadIst))
				except ValueError:
					logging.warning("["+str(calendar.timegm(time.gmtime()))+"] Case " + inputArr.case + " Ignoring header or empty data")

	currencyPairObj = econCurrencyPair(pairMember1,pairMember2,path,currencyPairEntryArr)
	# Create a calculator object and start calling the calculation methods
	econSummaryResultObj = econSummaryResult()
	econCalculatorObj = econCalculator(inputArr, currencyPairObj, econSummaryResultObj)
	logging.info("["+str(calendar.timegm(time.gmtime()))+"] Calculating Intermediate and Summary results => Case: " + inputArr.case + " Currency 1: " + pairMember1 + " Currency 2: " + pairMember2)
	econCalculatorObj.calculateAll()

	logging.info("["+str(calendar.timegm(time.gmtime()))+"] Calculating Summary results => Case: " + inputArr.case + " Currency 1: " + pairMember1 + " Currency 2: " + pairMember2)
	with open('./output/summary/summary_results_'+str(inputArr.case)+'_'+str(pairMember1)+'_'+str(pairMember2)+'_'+str(calendar.timegm(time.gmtime()))+'.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['Case','Weekend Timeout','Max Spread','Activity Criterion','Invert EMA','BuyRSI','BuyEMADist','SellRSI','SellEMADist','Take Profit','Stop Loss','BUYs Opened','Buys Take Profit','Buys Stop Loss','BUYs Closed','BUY Points','SELLs Opened','Sells Take Profit','Sells Stop Loss','SELLs Closed','SELL Points','Total Trades','Total Wins','Total Losses','Total Losses','Total Points'])
		writer.writerow([ inputArr.case,inputArr.weekendTimeout, inputArr.maxSpread, inputArr.activityCriterion, inputArr.invertEMA, inputArr.buyRSI, inputArr.buyEMADist, inputArr.sellRSI, inputArr.sellEMADist, inputArr.takeProfit, inputArr.stopLoss, str(econCalculatorObj.econSummaryResultObj.getbuysOpened()), str(econCalculatorObj.econSummaryResultObj.getbuysTakeProfit()), str(econCalculatorObj.econSummaryResultObj.getbuysStopLoss()), str(econCalculatorObj.econSummaryResultObj.getbuysClosed()), str(econCalculatorObj.econSummaryResultObj.getbuyPoints()), str(econCalculatorObj.econSummaryResultObj.getsellsOpened()), str(econCalculatorObj.econSummaryResultObj.getsellsTakeProfit()), str(econCalculatorObj.econSummaryResultObj.getsellsStopLoss()), str(econCalculatorObj.econSummaryResultObj.getsellsClosed()), str(econCalculatorObj.econSummaryResultObj.getsellPoints()), str(econCalculatorObj.econSummaryResultObj.gettotalTrades()), str(econCalculatorObj.econSummaryResultObj.gettotalWins()), str(econCalculatorObj.econSummaryResultObj.gettotalLosses1()), str(econCalculatorObj.econSummaryResultObj.gettotalLosses2()), str(econCalculatorObj.econSummaryResultObj.gettotalPoints()) ])
		
	if str(inputArr.calculateDetailed) == "1":
		logging.info("["+str(calendar.timegm(time.gmtime()))+"] Calculating Detailed results => Case: " + inputArr.case + " Currency 1: " + pairMember1 + " Currency 2: " + pairMember2)
		with open('./output/detailed/detailed_results_'+str(inputArr.case)+'_'+str(pairMember1)+'_'+str(pairMember2)+'_'+str(calendar.timegm(time.gmtime()))+'.csv', 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['TradeNo','Open DateTime','Open Price','Close DateTime','Close Price','Duration','Type','Points','Close Method'])
			detailedResultsArray = getDetailedResults(econCalculatorObj)
			for dr in detailedResultsArray:
				writer.writerow([dr.tradeNo, dr.openDateTime, dr.openPrice, dr.closeDateTime, dr.closePrice, dr.duration, dr.typeIndicator, dr.points, dr.closeMethod])

def getTradeData(item,itemset,tradetype,readrow,writerow):
	econDetailedResultEntryObj = econDetailedResultEntry("","","","","","","","","")
	tradeclosedatetime = ""
	tradeopenprice = ""
	tradepoints = ""
	tradeclosemethod = ""
	tradeduration = ""
	tradeopendatetime = ""
	tradecloseprice = ""

	if tradetype == "BUY" :
		rowCounter = 0;
		for items in itemset.currencyPair.cpFiles:
			if rowCounter == readrow:
				tradeopendatetime = items.timeUTC
				tradeopenprice = items.result.getBuyPrice()
				#print "DBG 1 BUY: " + str(tradeopenprice) + " => " + str(tradeopendatetime)
			rowCounter = rowCounter + 1

		rowCounter = 0;
		for items in itemset.currencyPair.cpFiles:
			if rowCounter > readrow:
				if str(items.result.getBuyCloseFlag()) == "" and str(items.result.getBuyRunningProfit()) != "":
					#print "DBG 4 BUY: " + str(items.result.getBuyCloseFlag()) + "=>" + str(items.result.getBuyRunningProfit())
					readrow = readrow + 1
					tradeclosedatetime = items.timeUTC
					tradecloseprice = items.bid1
					tradepoints = items.result.getBuyRunningProfit()
					tradeclosemethod = items.result.getBuyCloseFlag()
					try:
						#print "SELL: " + str(tradeclosedatetime) + "-" + str(tradeopendatetime)
						tradeduration = datetime.strptime(tradeclosedatetime,"%d/%m/%Y %H:%M:%S") - datetime.strptime(tradeopendatetime,"%d/%m/%Y %H:%M:%S")
					except:
						tradeduration = datetime.strptime(tradeclosedatetime,"%d/%m/%Y %H:%M") - datetime.strptime(tradeopendatetime,"%d/%m/%Y %H:%M")
				else:
					break
			rowCounter = rowCounter + 1
	else:
		rowCounter = 0;
		for items in itemset.currencyPair.cpFiles:
			if rowCounter == readrow:
				tradeopendatetime = items.timeUTC
				tradeopenprice = items.result.getSellPrice()
				#print "DBG 1 SELL: " + str(tradeopenprice) + " => " + str(tradeopendatetime)
			rowCounter = rowCounter + 1

		rowCounter = 0;
		for items in itemset.currencyPair.cpFiles:
			if rowCounter > readrow:
				if str(items.result.getSellCloseFlag()) == "" and str(items.result.getSellRunningProfit()) != "" :
					#print "DBG 4 SELL:" + str(items.result.getSellCloseFlag()) + "=" + str(items.result.getSellRunningProfit())
					readrow = readrow + 1
					tradeclosedatetime = items.timeUTC
					tradecloseprice = items.ask1
					tradepoints = items.result.getSellRunningProfit()
					tradeclosemethod = items.result.getSellCloseFlag()
					try:
						#print "SELL: " + str(tradeclosedatetime) + "-" + str(tradeopendatetime)
						tradeduration = datetime.strptime(tradeclosedatetime,"%d/%m/%Y %H:%M:%S") - datetime.strptime(tradeopendatetime,"%d/%m/%Y %H:%M:%S")
					except:
						tradeduration = datetime.strptime(tradeclosedatetime,"%d/%m/%Y %H:%M") - datetime.strptime(tradeopendatetime,"%d/%m/%Y %H:%M")
				else:
					break
			rowCounter = rowCounter + 1

	econDetailedResultEntryObj.tradeNo = writerow
	econDetailedResultEntryObj.openDateTime = tradeopendatetime
	econDetailedResultEntryObj.openPrice = tradeopenprice
	#print "DBG 1: " + str(writerow) + "=" + str(tradeopendatetime) + "=" + str(tradeopenprice) + "=" + str(tradeclosedatetime) + "=" + str(tradeclosedatetime) + " "
	if str(tradeclosedatetime) != "":

		econDetailedResultEntryObj.closeDateTime = tradeclosedatetime
		econDetailedResultEntryObj.closePrice = tradecloseprice
		econDetailedResultEntryObj.duration = tradeduration
		econDetailedResultEntryObj.typeIndicator = tradetype
		econDetailedResultEntryObj.points = tradepoints
		econDetailedResultEntryObj.closeMethod = tradeclosemethod
	else:
		econDetailedResultEntryObj.closeMethod = "Not Closed"
	return econDetailedResultEntryObj
	
def getDetailedResults(econCalculatorObj):
	readrow = 0
	writerow = 0
	testdate = econCalculatorObj.currencyPair.cpFiles[0].timeUTC
	detailedResultsArray = []	

	readrow = 0
	testdate = econCalculatorObj.currencyPair.cpFiles[0].timeUTC
	itemCounter = 0
	for items in econCalculatorObj.currencyPair.cpFiles:
		if str(items.result.getBuyFlag()) == "X":
			#logging.info("["+str(calendar.timegm(time.gmtime()))+"] Getting trade data: BUY " + str(readrow) + " " + str(writerow))
			detailedResultsArray.append(getTradeData(items,econCalculatorObj,"BUY",readrow,writerow))

		if str(items.result.getSellFlag()) == "X":
			#logging.info("["+str(calendar.timegm(time.gmtime()))+"] Getting trade data: SELL " + str(readrow) + " " + str(writerow))
			detailedResultsArray.append(getTradeData(items,econCalculatorObj,"SELL",readrow,writerow))
			writerow = writerow + 1
		readrow = readrow + 1
		itemCounter = itemCounter + 1
		if itemCounter % 20000 == 0:
			print "Detailed Results: " + str(round((itemCounter*100)/len(econCalculatorObj.currencyPair.cpFiles))) + "% completed..."
#    lastrow = Worksheets("DetailedResults").Cells(Rows.Count, "B").End(xlUp).Row
#    Worksheets("DetailedResults").Range("B2").Select
#    Worksheets("DetailedResults").Range(Selection, Selection.End(xlDown)).Select
#    Worksheets("DetailedResults").Range(Selection, Selection.End(xlToRight)).Select
#    Worksheets("DetailedResults").Sort.SortFields.Clear
#    Worksheets("DetailedResults").Sort.SortFields.Add Key:=Range("B2:B" & lastrow), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:=xlSortNormal
#    With Worksheets("DetailedResults").Sort
#        .SetRange Range("B1:I" & lastrow)
#        .Header = xlYes
#        .MatchCase = False
#        .Orientation = xlTopToBottom
#        .SortMethod = xlPinYin
#        .Apply
#    End With
#    Worksheets("DetailedResults").Range("A2").Select    
#    If Worksheets("SummaryResults").Range("U2").Value <> 0 Then
#    
#        Worksheets("DetailedResults").Range("A2").FormulaR1C1 = "1"
#        Worksheets("DetailedResults").Range("A3").Select
#        Worksheets("DetailedResults").Range("A3").FormulaR1C1 = "=R[-1]C+1"
#        Worksheets("DetailedResults").Range("A3").Select
#        Selection.AutoFill Destination:=Worksheets("DetailedResults").Range("A3:A" & lastrow)
#        Application.Calculate
#        Worksheets("DetailedResults").Range("A2").Select
#        Worksheets("DetailedResults").Range(Selection, Selection.End(xlDown)).Select
#        Selection.Copy
#        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks:=False, Transpose:=False
#        Worksheets("DetailedResults").Range("A2").Select
#        Application.CutCopyMode = False
#    Else
#    End If
	return detailedResultsArray
	
def econCalculation(inputArr):
	logging.info("["+str(calendar.timegm(time.gmtime()))+"] Starting Case thread: " + inputArr.case + " from thread " + threading.current_thread().name)
	path = "./currencypairs/"

	lst=os.listdir(path)
	currencyPairs = groupByPrefix(lst,"-")
	for pair,fileids in currencyPairs.iteritems():
		currencyPairThread = Thread(target=spawnCurrencyPairThread,args=(inputArr,pair[:3],pair[3:6],path,fileids))
		currencyPairThread.start()
		currencyPairThread.join()
		sleep(1)
