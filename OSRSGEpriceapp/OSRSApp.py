import os
import requests
from sqlalchemy import Integer, column
import GEIDs
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import *
from pandas import DataFrame

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    'From': 'joe.sealy@hotmail.co.uk' 
}

latestURLBase = "http://prices.runescape.wiki/api/v1/osrs/latest?id="
mappingURL = "http://prices.runescape.wiki/api/v1/osrs/mapping"
timeseriesURLBase ="http://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id="
app = Tk()





def intToString(integer):
    temp = int(Integer)
    as_string = str(temp)
    return as_string

def searchList(char):
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
    
def toUpper(Item):
    itemCharList = list(Item)
    itemCharCap = itemCharList[0].upper()
    itemCharList.pop(0)
    itemCharList.insert(0, itemCharCap)
    newItem = "".join(itemCharList)
    return newItem

def itemSearchFunction(Item):
    itemCharList = list(Item)
    itemList = searchList(itemCharList[0])
    itemID = [column[1] for column in itemList  if column[0]==Item]
    return(itemID.pop())

def formatDataPrice(ID, link):
    high = str(link["data"][ID]["high"]) + "gp"
    highTime = datetime.datetime.fromtimestamp(
        (link["data"][ID]["highTime"])
    ).strftime('%Y-%m-%d %H:%M:%S')

    low = str(link["data"][ID]["low"]) + "gp"
    lowTime = datetime.datetime.fromtimestamp( 
        (link["data"][ID]["lowTime"])
    ).strftime('%Y-%m-%d %H:%M:%S')
    data = [high, highTime, low, lowTime]
    return data

def formatDataGraph(link):
    timestamp = [] 
    avgHighPrice = [] 
    avgLowPrice = [] 
    highPriceVol = []
    lowPriceVol = []
    singleTimeStamp = datetime.datetime.fromtimestamp( 
        (link["data"][299]["timestamp"])
        ).strftime('%d-%m')
    
    print(singleTimeStamp)

    for x in range(288 , 299):
        TimeStamp = datetime.datetime.fromtimestamp( 
        (link["data"][x]["timestamp"])
        ).strftime('%H:%M')
        timestamp.append(TimeStamp)
        avgHighPrice.append(link["data"][x]["avgHighPrice"])
        avgLowPrice.append(link["data"][x]["avgLowPrice"])
        highPriceVol.append(link["data"][x]["highPriceVolume"])
        lowPriceVol.append(link["data"][x]["lowPriceVolume"])
    data1 = {"timestamp": timestamp,
             "avgHighPrice":avgHighPrice,
             "avgLowPrice": avgLowPrice
    }
    data2 = {"timestamp": timestamp,
             "highPriceVol":highPriceVol,
             "lowPriceVol": lowPriceVol
    }

    df1 = DataFrame(data1, columns = ["timestamp", "avgHighPrice", "avgLowPrice"])
    df2 = DataFrame(data2, columns = ["timestamp", "highPriceVol", "lowPriceVol"])


    figure = plt.Figure(figsize=(9,5), dpi=100)
    ax = figure.add_subplot(111)
    ax.scatter(df2["timestamp"],df2["highPriceVol"], color = "g")
    ax.scatter(df2["timestamp"],df2["lowPriceVol"], color = "r")
    ax.legend(["highPriceVol"]) 
    ax.set_xlabel("timestamp")
    ax.set_title(singleTimeStamp + ("latest hour to item volume"))

def nameToID():
    itemName = rs_item_entry.get()
    itemName = toUpper(itemName)
    itemIDstr = itemSearchFunction(itemName)
    return itemIDstr

def latestPrice():
    itemIDstr = nameToID()
    latestURL = latestURLBase + itemIDstr 
    RSGElatest = requests.get(latestURL, headers = headers)
    RSGE = RSGElatest.json()
    #{"data":{"4151":{"high":2055472,"highTime":1643731540,"low":2024505,"lowTime":1643731632}}}
    data = formatDataPrice( itemIDstr, RSGE)
    display(data)

def display(data):
    display.high = data[0]
    display.highTime = data[1]
    display.low = data[2]
    display.lowTime = data[3]

def mappingURL():
    RSGEmapping = requests.get(mappingURL, headers = headers)

def timeseriesURL():
    itemIDstr = nameToID()
    timeseriesURL = timeseriesURLBase + itemIDstr
    RSGEtimeseries = requests.get(timeseriesURL, headers = headers)
    RSGEtime = RSGEtimeseries.json()
    data = formatDataGraph(RSGEtime)

#Parts
rs_item_text = StringVar()

rs_item_label = Label(app, text = "OSRS Item Name", font = ("Bold", 10), pady = 20)
rs_item_label.grid(row=0, column=0, sticky=E)

rs_item_entry=Entry(app, textvariable=rs_item_text)
rs_item_entry.grid(row=0,column=1)

rs_item_search_button = Button(app, text = "Search", width = 5, command = latestPrice)
rs_item_search_button.grid(row=0, column=2, pady=20)

rs_item_graph_button = Button(app, text = "Map", width = 5, command = timeseriesURL)
rs_item_graph_button.grid(row=0, column=3, pady=20)

rs_high_price= Label(app, text = "High Price:   " +  display.high, font = ("Bold", 10), pady = 20)
rs_high_price.grid(row=3, column=1, sticky=NSEW)

rs_high_Time = Label(app, text = "High Price Time:   " + display.highTime, font = ("Bold", 10), pady = 20)
rs_high_Time.grid(row=4, column=1, sticky=NSEW)

rs_low_price = Label(app, text = "Low Price:    " + display.low, font = ("Bold", 10), pady = 20)
rs_low_price.grid(row=5, column=1, sticky=NSEW)

rs_low_Time = Label(app, text = "Low Price Time:   " + display.lowTime, font = ("Bold", 10), pady = 20)
rs_low_Time.grid(row=6, column=1, sticky=NSEW)

scatter3 = FigureCanvasTkAgg(figure, app) 
scatter3.get_tk_widget().grid(row = 3, column = 5, rowspan =  9, columnspan = 5)

app.title("OSRS GE Guru")                                            
app.geometry("1400x700")

app.mainloop()



