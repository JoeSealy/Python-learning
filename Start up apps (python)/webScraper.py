import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
import time
import base64 
import os
import personal
from email.message import EmailMessage

EMAIL_ADD = personal.EMAIL_ADDRESS
EMAIL_PASS = personal.EMAIL_PASSWORD

URL = "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1311&_nkw=1070ti+graphics+card&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=GRAPHICS+CARDS&_osacat=0&LH_All=1"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

def data_get(URL):
    request = requests.get(URL, headers = header)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup



def data_find(soup):
    message = []
    results = soup.find_all("li", class_ = "s-item s-item__pl-on-bottom s-item--watch-at-corner", limit = 20)
    for products in results:

        title = products.find("h3", class_ ="s-item__title").text
        condition = products.find("span", class_ = "SECONDARY_INFO").text
        sellingPrice = products.find("span", class_ = "s-item__price").text
        timeLeft = products.find("span", class_ = "s-item__time-left")
        bids = products.find("span", class_ = "s-item__bids s-item__bidCount")
        buyItNow = products.find("span", class_ = "s-item__purchase-options-with-icon")
        link = products.find("a", class_ = "s-item__link")["href"]

        if buyItNow == None :
            buyItNow = "NaN"
            bids = bids.text
            timeLeft = timeLeft.text
        else:
            buyItNow = "Yes"
            bids = "NaN"
            timeLeft = "NaN"

        sellingTemp = sellingPrice.split("£")
        AsciiSellingPoint = (sellingTemp[1] + " Pounds")

        first_char = condition[0]
        if(first_char == "O"):
            condition = "Opened But Never Used"
        elif(first_char == "P"):
            condition = "Pre owned"

        each_product = {
            f"Title: {title}\n Condition: {condition}\n Selling Price: {AsciiSellingPoint}\n Time Left: {timeLeft}\n Bids: {bids}\n Buy it Now?: {buyItNow}\n Link: {link}\n"
        }

        message.append(each_product) 
        
    return message

def send_mail(message):
    msg = EmailMessage()
    msg['Subject'] = "Some Graphics cards Poo Boy"
    msg['From'] = EMAIL_ADD
    msg['To'] = "joe.sealy@hotmail.co.uk"
    msg.set_content(message)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.login(EMAIL_ADD, EMAIL_PASS)
        smtp.send_message(msg)
        print("mail has been sent")
        smtp.quit()


#while(True):
#    check_price()
#   time.sleep(60)

data = data_get(URL)
message = data_find(data)
print(message)
#send_mail(message)