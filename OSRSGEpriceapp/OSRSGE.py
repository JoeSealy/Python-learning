import os
import requests
import GEIDs
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer


class OSRSApp:
    def __init__(self, app):

        self.inputs()
    
    def inputs(self):
        self.rs_item_label = Label(app, text = "OSRS Item Name", font = ("Bold", 10), pady = 20)
        self.rs_item_label.grid(row=0, column=0, sticky=W)

        self.rs_item_text = StringVar()
        self.rs_item_entry = Entry(app, textvariable = self.rs_item_text)
        self.rs_item_entry.grid(row=0,column=1, sticky=W)

        self.rs_item_search_button = Button(app, text = "Search", width = 5, command = self.displayData)
        self.rs_item_search_button.grid(row=0, column=2, pady=20)

        self.full_Top_Graph_Button= Button(app, text = " Top Full Graph", width = 6, command = self.topFullGraphcall)
        self.full_Top_Graph_Button.grid(row=0, column=3, pady=20, columnspan=2)

        self.full_Bottom_Graph_Button= Button(app, text = "Bottom Full Graph", width = 6, command = self.bottomFullGraphcall)
        self.full_Bottom_Graph_Button.grid(row=0, column=5, pady=20, columnspan=2)


    def displayData(self):

        numericalData, dfPriceAll, dfVolAll = coolData.doFunctionality(coolData, self.rs_item_text.get())

        self.clearWidgets()
        self.inputs()

        dfPriceTwelve = []
        dfVolTwelve = []

        dfPriceTwelve = dfPriceAll.loc[288:299]
        dfVolTwelve = dfVolAll.loc[288:299]

        self.rs_high_price= Label( text = "High Price:   " +  numericalData[0], font = ("Bold", 10), pady = 20)
        self.rs_high_price.grid(row=3, column=0, sticky=W)

        self.rs_high_Time = Label(text = "High Price Time:   " + numericalData[1], font = ("Bold", 10), pady = 20)
        self.rs_high_Time.grid(row=4, column=0, sticky=NSEW)

        self.rs_low_price = Label(text = "Low Price:    " + numericalData[2], font = ("Bold", 10), pady = 20)
        self.rs_low_price.grid(row=5, column=0, sticky=W)

        self.rs_low_Time = Label(text = "Low Price Time:   " + numericalData[3], font = ("Bold", 10), pady = 20)
        self.rs_low_Time.grid(row=6, column=0, sticky=NSEW)

        self.figure = plt.Figure(figsize=(40,10),dpi=100)
        ax = self.figure.add_subplot(111)
        ax.scatter(dfPriceAll["timestamp"], dfPriceAll["avgHighPrice"], color = "g")
        ax.scatter(dfPriceAll["timestamp"], dfPriceAll["avgLowPrice"], color = "r")
        ax.legend(["avgPrice"]) 
        ax.set_xlabel("timestamp")

        self.figure1 = plt.Figure(figsize=(40,10), dpi=100)
        ax1 = self.figure1.add_subplot(111)
        ax1.scatter(dfVolAll["timestamp"], dfVolAll["highPriceVol"], color = "g")
        ax1.scatter(dfVolAll["timestamp"], dfVolAll["lowPriceVol"], color = "r")
        ax1.legend(["Vol"]) 
        ax1.set_xlabel("timestamp")
        
        figure2 = plt.Figure(figsize=(6,3),dpi=100)
        ax2 = figure2.add_subplot(111)
        ax2.scatter(dfPriceTwelve["timestamp"],dfPriceTwelve["avgHighPrice"], color = "g")
        ax2.scatter(dfPriceTwelve["timestamp"],dfPriceTwelve["avgLowPrice"], color = "r")
        ax2.legend(["avgPrice"]) 
        ax2.set_xlabel("timestamp")

        scatter2 = FigureCanvasTkAgg(figure2, app) 
        scatter2.get_tk_widget().grid(row = 3, column = 5, rowspan =  20, columnspan = 20)

        figure3 = plt.Figure(figsize=(6,3), dpi=100)
        ax3 = figure3.add_subplot(111)
        ax3.scatter(dfVolTwelve["timestamp"],dfVolTwelve["highPriceVol"], color = "g")
        ax3.scatter(dfVolTwelve["timestamp"],dfVolTwelve["lowPriceVol"], color = "r")
        ax3.legend(["Vol"]) 
        ax3.set_xlabel("timestamp")

        scatter3 = FigureCanvasTkAgg(figure3, app) 
        scatter3.get_tk_widget().grid(row = 24, column = 5, rowspan =  20, columnspan = 20)

    def clearWidgets(self):
        for widgets in app.winfo_children():
            widgets.destroy()

    def topFullGraphcall(self):

        topfullgraph = Toplevel()
        topfullgraph.geometry("2100x1400")
        scatter = FigureCanvasTkAgg(self.figure, topfullgraph) 
        scatter.get_tk_widget().pack()
        
    def bottomFullGraphcall(self):

        bottomfullgraph = Toplevel()
        bottomfullgraph.geometry("2100x1400")
        scatter1 = FigureCanvasTkAgg(self.figure1, bottomfullgraph)
        scatter1.get_tk_widget().pack()

class coolData():
    def __init__(self):
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        'From': 'joe.sealy@hotmail.co.uk' 
        }

        self.latestURLBase = "http://prices.runescape.wiki/api/v1/osrs/latest?id="
        self.mappingURL = "http://prices.runescape.wiki/api/v1/osrs/mapping"
        self.timeseriesURLBase ="http://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id="
        #{"data":{"4151":{"high":2055472,"highTime":1643731540,"low":2024505,"lowTime":1643731632}}}

    def doFunctionality(self, itemName): 
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        'From': 'joe.sealy@hotmail.co.uk' 
        }
        self.timeseriesURLBase ="http://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id="
        self.latestURLBase = "http://prices.runescape.wiki/api/v1/osrs/latest?id="

        #Numerical display data
        capsItemName    = self.toUpper(self, itemName)                              # caps the first letter if not already
        itemCharList    = self.stringToList(self, capsItemName)                     # makes the string to a list
        itemList        = self.searchList(self, itemCharList[0])                    # finds the right list using the first initial
        itemIDstr       = self.ItemIDSearch(self, itemList, capsItemName)           # finds ID using the name of item
        osrsPriceURL    = self.concat(self, self.latestURLBase, itemIDstr)          # concats the id with link
        RSGEPrice       = self.getRequests(self, osrsPriceURL, self.headers)        # requests api info using the link
        RSGE            = self.dotJSON(self, RSGEPrice)                             # .JSON recieves info
        numericalData   = self.formatDataPrice(self, itemIDstr, RSGE)               # formats the data and returns whats needed
        
        #Graphical display data
        timeseriesURL   = self.concat(self, self.timeseriesURLBase, itemIDstr)
        RSGEtimeseries  = self.getRequests(self, timeseriesURL, self.headers)
        RSGEtime        = self.dotJSON(self, RSGEtimeseries)
        dfPriceAll, dfVolAll = self.formatDataGraph(RSGEtime)
        predictedPrice = self.predict(self, dfPriceAll, dfVolAll)



        return (numericalData, dfPriceAll, dfVolAll)

    def dotJSON(self, data):
        return data.json()

    def getRequests(self, url, headers):
        request = requests.get(url, headers = headers)
        return request

    def toUpper(self, Item):
        itemCharList = list(Item)
        itemCharCap = itemCharList[0].upper()
        itemCharList.pop(0)
        itemCharList.insert(0, itemCharCap)
        newItem = "".join(itemCharList)
        return newItem

    def searchList(self, char):
        if char == "A":
            return GEIDs.AList
        elif char == "B":
            return GEIDs.BList
        elif char == "C":
            return GEIDs.CList
        elif char == "D":
            return GEIDs.DList
        elif char == "E":
            return GEIDs.EList
        elif char == "F":
            return GEIDs.FList
        elif char == "G":
            return GEIDs.GList
        elif char == "H":
            return GEIDs.HList
        elif char == "I":
            return GEIDs.IList
        elif char == "J":
            return GEIDs.JList
        elif char == "K":
            return GEIDs.KList
        elif char == "L":
            return GEIDs.LList
        elif char == "M":
            return GEIDs.MList
        elif char == "N":
            return GEIDs.NList
        elif char == "O":
            return GEIDs.OList
        elif char == "P":
            return GEIDs.PList
        elif char == "Q":
            return GEIDs.QList
        elif char == "R":
            return GEIDs.RList
        elif char == "S":
            return GEIDs.SList
        elif char == "T":
            return GEIDs.TList
        elif char == "U":
            return GEIDs.UList
        elif char == "V":
            return GEIDs.VList
        elif char == "X":
            return GEIDs.XList
        elif char == "Y":
            return GEIDs.YList
        elif char == "Z":
            return GEIDs.ZList
        elif char == "3":
            return GEIDs.thirdList
        elif char == "%":
            return GEIDs.lastUpdate

    def intToString(self, integer):
        temp = int(integer)
        as_string = str(temp)
        return as_string

    def formatDataPrice(self , ID, link):
        high = str(link["data"][ID]["high"]) + "gp"
        highTime =  dt.datetime.fromtimestamp(
            (link["data"][ID]["highTime"])
        ).strftime('%Y-%m-%d %H:%M:%S')

        low = str(link["data"][ID]["low"]) + "gp"
        lowTime = dt.datetime.fromtimestamp( 
            (link["data"][ID]["lowTime"])
        ).strftime('%Y-%m-%d %H:%M:%S')
        data = [high, highTime, low, lowTime]
        return data
    
    def stringToList(self, item):
        charList = list(item)
        return charList

    def ItemIDSearch(self, itemList, Item):
        itemID = [column[1] for column in itemList  if column[0]==Item]
        return(itemID.pop())

    def concat(self, a,b):
        return(a+b)

    def formatDataGraph(link):
        timestamp = [] 
        avgHighPrice = [] 
        avgLowPrice = [] 
        highPriceVol = []
        lowPriceVol = []

        singleTimeStamp = dt.datetime.fromtimestamp( 
            (link["data"][299]["timestamp"])
            ).strftime('%d-%m')

        for x in range(0 , 299):
            TimeStamp = dt.datetime.fromtimestamp( 
            (link["data"][x]["timestamp"])
            ).strftime('%H%M')
            timestamp.append(TimeStamp)
                

            if link["data"][x]["avgHighPrice"] == None:
                link["data"][x]["avgHighPrice"] = link["data"][x - 1]["avgHighPrice"]

            if link["data"][x]["avgLowPrice"] == None:
                link["data"][x]["avgLowPrice"] = link["data"][x - 1]["avgLowPrice"]

            avgHighPrice.append(link["data"][x]["avgHighPrice"])
            avgLowPrice.append(link["data"][x]["avgLowPrice"])
            highPriceVol.append(link["data"][x]["highPriceVolume"])
            lowPriceVol.append(link["data"][x]["lowPriceVolume"])

        listpriceAll = {"timestamp": timestamp,
                "avgHighPrice":avgHighPrice,
                "avgLowPrice": avgLowPrice
        }
        listvolAll = {"timestamp": timestamp,
                "highPriceVol":highPriceVol,
                "lowPriceVol": lowPriceVol
        }

        dfPriceAll = DataFrame(listpriceAll  , columns = ["timestamp", "avgHighPrice", "avgLowPrice"])
        dfVolAll = DataFrame(listvolAll , columns = ["timestamp", "highPriceVol", "lowPriceVol"])

        return(dfPriceAll, dfVolAll)

    def predict(self, prices, volumes):


        highY = prices["avgHighPrice"]
        highX = volumes[["highPriceVol"]]

        lowY = prices["avgLowPrice"]
        lowX = volumes[["timestamp","lowPriceVol"]]
        
        pd.set_option("display.max_rows", None)

        high_X_train, high_X_test, high_Y_train, high_Y_test = train_test_split(highX,highY, train_size=0.60)
        low_X_train, low_X_test, low_Y_train, low_Y_test = train_test_split(lowX,lowY, test_size=0.05)

        clf = LinearRegression()
        clf.fit(high_X_train, high_Y_train)
        clf.predict(high_X_test)
        
        accuracy = clf.score(high_X_test, high_Y_test)
        print(high_X_test)
        print(high_Y_test)
        print(accuracy)
        
app = Tk()
app.geometry("1400x700")
OSRSApp(app)
coolData()
app.title("OSRS GE Guru")
app.mainloop()