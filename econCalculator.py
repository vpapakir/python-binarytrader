from datetime import datetime
from econSummaryResult import econSummaryResult
import logging
import calendar
import time

logging.basicConfig(filename='./econ.log',level=logging.INFO)

class econCalculator:
	inputSet = []
	currencyPair = 0
	econSummaryResultObj = econSummaryResult()

	def __init__(self, inputSet, currencyPair, econSummaryResultObj):
		self.inputSet = inputSet
		self.currencyPair = currencyPair
		self.econSummaryResultObj = econSummaryResultObj

	def getInputSet(self):
		return self.inputSet

	def getCurrencyPair(self):
		return self.currencyPair

	def calculateTimeOut(self,iteration,inputSet,currItem,previousItem):
		if iteration == 1:
			currItem.result.timeOut = "X"
		else:
			if str(currItem.timeUTC) != "":
				try:
					val = float(previousItem.result.getTimeOut())
					if val > 0:
						currItem.result.setTimeOut(previousItem.result.timeOut - 1)
					else:
						currItem.result.setTimeOut("X")
				except ValueError:
					dTime1 = 0
					dTime2 = 0
					try:
						dTime1 = datetime.strptime(currItem.timeUTC,"%d/%m/%Y %H:%M:%S").weekday()
					except ValueError:
						dTime1 = datetime.strptime(currItem.timeUTC,"%d/%m/%Y %H:%M").weekday()
					try:
						dTime2 = datetime.strptime(previousItem.timeUTC,"%d/%m/%Y %H:%M:%S").weekday()
					except ValueError:
						dTime2 = datetime.strptime(previousItem.timeUTC,"%d/%m/%Y %H:%M").weekday()

					if (dTime1 == 6) and (dTime2 == 4):
						currItem.result.setTimeOut(inputSet.weekendTimeOut)
					else:
						currItem.result.setTimeOut("X")
			else:
				currItem.result.setTimeOut("")

		return currItem

	def calculateSpreadFlag(self,inputSet,currItem):
		if int(currItem.spread) <= int(inputSet.maxSpread) :
			currItem.result.setSpreadFlag("X")
		else :
			currItem.result.setSpreadFlag("")
		return currItem

	def calculateActivityFlag(self,inputSet,currItem):
		if float(currItem.atr) >= float(inputSet.activityCriterion) :
			currItem.result.setActivityFlag("X")
		else:
			currItem.result.setActivityFlag("")
		return currItem

	def calculateBuyRSI(self,inputSet,currItem):
		if float(currItem.rsi) >= float(inputSet.buyRSI) :
			currItem.result.setBuyRSI("X")
		else :
			currItem.result.setBuyRSI("")
		return currItem			

	def calculateBuyEMADist(self,inputSet,currItem):
		if int(inputSet.invertEMA) == 1:
			if float(currItem.emadIst) <= float(inputSet.buyEMADist) :
				currItem.result.setBuyEMADist("X")
			else:
				currItem.result.setBuyEMADist("")
		else:
			if float(currItem.emadIst) >= float(inputSet.buyEMADist) :
				currItem.result.setBuyEMADist("X")
			else:
				currItem.result.setBuyEMADist("")
		return currItem			

	def calculateBuyFlag(self,iteration,inputSet,currItem,previousItem):
		if iteration == 1:
			if (str(currItem.result.getTimeOut()) == "X") and (str(currItem.result.getSpreadFlag()) == "X") and str((currItem.result.getActivityFlag()) == "X") and str((currItem.result.getBuyRSI()) == "X") and str((currItem.result.getBuyEMADist()) == "X") :
				currItem.result.setBuyFlag("X")
			else:
				currItem.result.setBuyFlag("")
		else:
			if previousItem.result.getBuyCloseFlag() != "" :
				currItem.result.setBuyFlag("")
			else:
				if previousItem.result.getBuyPrice() != "":
					if ( str(currItem.result.getTimeOut()) == "X") and ( str(currItem.result.getSpreadFlag()) == "X") and ( str(currItem.result.getActivityFlag()) == "X") and ( str(currItem.result.getBuyRSI()) == "X") and ( str(currItem.result.getBuyEMADist()) == "X") :
						currItem.result.setBuyFlag("X")
					else:
						currItem.result.setBuyFlag("")
				else:
					currItem.result.setBuyFlag("")
		return currItem			
		
	def calculateBuyPrice(self,iteration,inputSet,currItem,previousItem):
		if int(iteration) == 1 :
			if str(currItem.result.getBuyFlag()) == "X" :
				currItem.result.setBuyPrice(currItem.ask1)
			else:
				currItem.result.setBuyPrice("")
		else:
			if str(previousItem.result.getBuyCloseFlag()) != "" :
				currItem.result.setBuyPrice("")
			else:
				if str(previousItem.result.getBuyPrice()) != "" :
					currItem.result.setBuyPrice(previousItem.result.getBuyPrice())
				else:
					if str(currItem.result.getBuyFlag()) == "X" :
						currItem.result.setBuyPrice(currItem.ask1)
					else:
						currItem.result.setBuyPrice("")
		return currItem

	def calculateBuyRunningProfit(self,iteration,inputSet,currItem):
		if iteration == 1:
			if currItem.result.getBuyPrice() != "" :
				currItem.result.setBuyRunningProfit(str(int(round((float(currItem.bid1)-float(currItem.result.getBuyPrice()))*100000))))
			else:
				currItem.result.setBuyRunningProfit("")
		else:
			if currItem.bid1 != "" :
				if currItem.result.getBuyPrice() != "" :
					currItem.result.setBuyRunningProfit(str(int(round((float(currItem.bid1)-float(currItem.result.getBuyPrice()))*100000))))
				else:
					currItem.result.setBuyRunningProfit("")
			else:
				currItem.result.setBuyRunningProfit("")
		return currItem

	def calculateBuyCloseFlag(self,iteration,inputSet,currItem):
		if iteration == 1:
			if str(currItem.result.getBuyPrice()) != "" :
				if float(currItem.result.getBuyRunningProfit()) >= float(inputSet.takeProfit) :
					currItem.result.setBuyCloseFlag("TAKE PROFIT")
				else:
					if float(currItem.result.getBuyRunningProfit()) <= ((-1)*(float(inputSet.stopLoss))) :
						currItem.result.setBuyCloseFlag("STOP LOSS")
					else:
						currItem.result.setBuyCloseFlag("")
			else:
				currItem.result.setBuyCloseFlag("")
		else:
			if str(currItem.timeUTC) != "":
				if str(currItem.result.getBuyPrice()) != "" :
					if float(currItem.result.getBuyRunningProfit()) >= float(inputSet.takeProfit) :
						currItem.result.setBuyCloseFlag("TAKE PROFIT")
					else:
						if float(currItem.result.getBuyRunningProfit()) <= float(((-1)*(float(inputSet.stopLoss)))) :
							currItem.result.setBuyCloseFlag("STOP LOSS")
						else:
							currItem.result.setBuyCloseFlag("")
				else:
					currItem.result.setBuyCloseFlag("")
			else:
				currItem.result.setBuyCloseFlag("")
		return currItem
		
	def calculateSellRSI(self,inputSet,currItem):
		if float(currItem.rsi) >= float(inputSet.sellRSI) :
			currItem.result.setSellRSI("X")
		else:
			currItem.result.setSellRSI("")
		return currItem

	def calculateSellEMADist(self,inputSet,currItem):
		if str(inputSet.invertEMA) != "" :
			if  float(currItem.emadIst) >= float(inputSet.sellEMADist) :
				currItem.result.setSellEMADist("X")
			else:
				currItem.result.setSellEMADist("")
		else:
			if float(currItem.emadIst) <= float(inputSet.sellEMADist) : 
				currItem.result.setSellEMADist("X")
			else:
				currItem.result.setSellEMADist("")
		return currItem

	def calculateSellFlag(self,iteration,inputSet,currItem,previousItem):
		if iteration == 1:
			if (str(currItem.result.getTimeOut()) == "X") and (str(currItem.result.getSpreadFlag()) == "X") and (str(currItem.result.getActivityFlag()) == "X") and (str(currItem.result.getSellRSI()) == "X") and (str(currItem.result.getSellEMADist()) == "X"):
				currItem.result.setSellFlag("X")
			else:
				currItem.result.setSellFlag("")
		else:
			if str(previousItem.result.getSellCloseFlag()) != "":
				currItem.result.setSellFlag("")
			else:
				if str(previousItem.result.getSellPrice()) != "":
					currItem.result.setSellFlag("")
				else:
					if (str(currItem.result.getTimeOut()) == "X") and (str(currItem.result.getSpreadFlag()) == "X") and (str(currItem.result.getActivityFlag()) == "X") and (str(currItem.result.getSellRSI()) == "X") and (str(currItem.result.getSellEMADist()) == "X"):
						currItem.result.setSellFlag("X")
					else:
						currItem.result.setSellFlag("")
		return currItem

	def calculateSellPrice(self,iteration,inputSet,currItem,previousItem):
		if iteration == 1:
			if str(currItem.result.getSellFlag()) == "X" :
				currItem.result.setSellPrice(currItem.bid1)
			else:
				currItem.result.setSellPrice("")
		else:
			if str(previousItem.result.getSellCloseFlag()) != "" :
				currItem.result.setSellPrice("")
			else:
				if str(previousItem.result.getSellPrice()) != "" :
					currItem.result.setSellPrice(previousItem.result.getSellPrice())
				else:
					if str(currItem.result.getSellFlag()) == "X" :
						currItem.result.setSellPrice(currItem.ask1)
					else:
						currItem.result.setSellPrice("")
		return currItem

	def calculateSellRunningProfit(self,iteration,inputSet,currItem):
		if iteration == 1:
			if str(currItem.result.getSellPrice()) != "":
				currItem.result.setSellRunningProfit(str(int(round((float(currItem.result.getSellPrice())-float(currItem.ask1))*100000))))
			else:
				currItem.result.setSellRunningProfit("")
		else:
			if str(currItem.ask1) != "":
				if str(currItem.result.getSellPrice()) != "":
					currItem.result.setSellRunningProfit(str(int(round((float(currItem.result.getSellPrice())-float(currItem.ask1))*100000))))
				else:
					currItem.result.setSellRunningProfit("")
			else:
				currItem.result.setSellRunningProfit("")
		return currItem

	def calculateSellCloseFlag(self,iteration,inputSet,currItem):
		if iteration == 1:
			if str(currItem.result.getSellPrice()) != "":
				if float(currItem.result.getSellRunningProfit()) >= float(inputSet.takeProfit) :
					currItem.result.setSellCloseFlag("TAKE PROFIT")
				else:
					if float(currItem.result.getSellRunningProfit()) <= (float(inputSet.stopLoss)*(-1)) :
						currItem.result.setSellCloseFlag("STOP LOSS")
					else:
						currItem.result.setSellCloseFlag("")
			else:
				currItem.result.setSellCloseFlag("")
		else:
			if str(currItem.timeUTC) != "":
				if str(currItem.result.getSellPrice()) != "":
					if float(currItem.result.getSellRunningProfit()) >= float(inputSet.takeProfit):
						currItem.result.setSellCloseFlag("TAKE PROFIT")
					else:
						if float(currItem.result.getSellRunningProfit()) <= (float(inputSet.stopLoss)*(-1)) :
							currItem.result.setSellCloseFlag("STOP LOSS")
						else:
							currItem.result.setSellCloseFlag("")
				else:
					currItem.result.setSellCloseFlag("")
			else:
				currItem.result.setSellCloseFlag("")
		return currItem

	def calculateAll(self):
		firstIter = 1
		itemCounter = 0

		for items in self.currencyPair.cpFiles:
			previous = items
			if firstIter == 1 :
				items = self.calculateTimeOut(1,self.inputSet,items,previous)
				items = self.calculateSpreadFlag(self.inputSet,items)
				items = self.calculateActivityFlag(self.inputSet,items)
				items = self.calculateBuyRSI(self.inputSet,items)
				items = self.calculateBuyEMADist(self.inputSet,items)

				items = self.calculateBuyFlag(1,self.inputSet,items,previous)
				if str(items.result.buyFlag) == "X":
					self.econSummaryResultObj.setbuysOpened(self.econSummaryResultObj.getbuysOpened()+1)

				items = self.calculateBuyPrice(1,self.inputSet,items,previous)
				items = self.calculateBuyRunningProfit(1,self.inputSet,items)
				tmp1 = 0
				tmp2 = 0
				if str(items.result.buyCloseFlag) == "TAKE PROFIT":
					tmp1 = tmp1 + items.result.getBuyRunningProfit
				if str(items.result.buyCloseFlag) == "STOP LOSS":
					tmp2 = tmp2 + items.result.getBuyRunningProfit
				self.econSummaryResultObj.setbuyPoints(tmp1 + tmp2)

				items = self.calculateBuyCloseFlag(1,self.inputSet,items)
				if str(items.result.buyCloseFlag) == "TAKE PROFIT":
					self.econSummaryResultObj.setbuysTakeProfit(self.econSummaryResultObj.getbuysTakeProfit()+1)
				if str(items.result.buyCloseFlag) == "STOP LOSS":
					self.econSummaryResultObj.setbuysStopLoss(self.econSummaryResultObj.getbuysStopLoss()+1)
				self.econSummaryResultObj.setbuysClosed(self.econSummaryResultObj.getbuysStopLoss()+self.econSummaryResultObj.getbuysTakeProfit())

				items = self.calculateSellRSI(self.inputSet,items)
				items = self.calculateSellEMADist(self.inputSet,items)

				items = self.calculateSellFlag(1,self.inputSet,items,previous)
				if str() == "X":
					self.econSummaryResultObj.setsellsOpened(self.econSummaryResultObj.getsellsOpened() + 1)

				items = self.calculateSellPrice(1,self.inputSet,items,previous)	
				items = self.calculateSellRunningProfit(1,self.inputSet,items)

				items = self.calculateSellCloseFlag(1,self.inputSet,items)
				if str(items.result.sellCloseFlag)  == "TAKE PROFIT":
					self.econSummaryResultObj.setsellsTakeProfit(self.econSummaryResultObj.getsellsTakeProfit() + 1)
				if str(items.result.sellCloseFlag)  == "STOP LOSS":
					self.econSummaryResultObj.setsellsStopLoss(self.econSummaryResultObj.getsellsStopLoss() + 1)				

				self.econSummaryResultObj.settotalLosses1(self.econSummaryResultObj.getbuysStopLoss() + self.econSummaryResultObj.getsellsStopLoss())				
				self.econSummaryResultObj.settotalLosses2(self.econSummaryResultObj.getbuysClosed() + self.econSummaryResultObj.getbuysClosed())
				self.econSummaryResultObj.settotalPoints(self.econSummaryResultObj.getsellsTakeProfit()+self.econSummaryResultObj.getsellPoints())
				firstIter = 0
			else:
				items = self.calculateTimeOut(0,self.inputSet,items,previous)
				items = self.calculateSpreadFlag(self.inputSet,items)
				items = self.calculateActivityFlag(self.inputSet,items)
				items = self.calculateBuyRSI(self.inputSet,items)
				items = self.calculateBuyEMADist(self.inputSet,items)

				items = self.calculateBuyFlag(0,self.inputSet,items,previous)
				if str(items.result.buyFlag) == "X":
					self.econSummaryResultObj.setbuysOpened(self.econSummaryResultObj.getbuysOpened()+1)

				items = self.calculateBuyPrice(0,self.inputSet,items,previous)
				items = self.calculateBuyRunningProfit(0,self.inputSet,items)

				items = self.calculateBuyCloseFlag(0,self.inputSet,items)
				if str(items.result.buyCloseFlag) == "TAKE PROFIT":
					self.econSummaryResultObj.setbuysTakeProfit(self.econSummaryResultObj.getbuysTakeProfit()+1)
				if str(items.result.buyCloseFlag) == "STOP LOSS":
					self.econSummaryResultObj.setbuysStopLoss(self.econSummaryResultObj.getbuysStopLoss()+1)

				self.econSummaryResultObj.setbuysClosed(self.econSummaryResultObj.getbuysTakeProfit() + self.econSummaryResultObj.getbuysStopLoss())

				items = self.calculateSellRSI(self.inputSet,items)
				items = self.calculateSellEMADist(self.inputSet,items)

				items = self.calculateSellFlag(0,self.inputSet,items,previous)
				if str() == "X":
					self.econSummaryResultObj.setsellsOpened(self.econSummaryResultObj.getsellsOpened() + 1)

				items = self.calculateSellPrice(0,self.inputSet,items,previous)	
				items = self.calculateSellRunningProfit(0,self.inputSet,items)

				items = self.calculateSellCloseFlag(0,self.inputSet,items)
				if str(items.result.sellCloseFlag)  == "TAKE PROFIT":
					self.econSummaryResultObj.setsellsTakeProfit(self.econSummaryResultObj.getsellsTakeProfit() + 1)
				if str(items.result.sellCloseFlag)  == "STOP LOSS":
					self.econSummaryResultObj.setsellsStopLoss(self.econSummaryResultObj.getsellsStopLoss() + 1)				

				self.econSummaryResultObj.settotalLosses1(self.econSummaryResultObj.getbuysStopLoss() + self.econSummaryResultObj.getsellsStopLoss())				
				self.econSummaryResultObj.settotalLosses2(self.econSummaryResultObj.getbuysClosed() + self.econSummaryResultObj.getbuysClosed())

				self.econSummaryResultObj.settotalPoints(self.econSummaryResultObj.getsellsTakeProfit()+self.econSummaryResultObj.getsellPoints()) 

			previous = items
			itemCounter = itemCounter + 1
			if itemCounter % 20000 == 0:
				print "Summary results: " + str(round(itemCounter*100)/len(self.currencyPair.cpFiles)) + "% completed..."

