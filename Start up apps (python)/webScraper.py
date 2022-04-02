import imghdr
import requests
import pandas as pd
import smtplib
import time
import base64 
import os

from sympy import content
import personal
import shutil 
from email.message import EmailMessage
from bs4 import BeautifulSoup

EMAIL_ADD = personal.EMAIL_ADDRESS
EMAIL_PASS = personal.EMAIL_PASSWORD
HEADER = personal.HEADER

URL = "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1311&_nkw=1070ti+graphics+card&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=GRAPHICS+CARDS&_osacat=0&LH_All=1"

def data_get(URL):
    request = requests.get(URL, headers = HEADER)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup



def data_find(soup):
    imageList = []
    productFeatureList = []
    msg = EmailMessage()
    msg['Subject'] = "Some Graphics cards Poo Boy"
    msg['From'] = EMAIL_ADD
    msg['To'] = "joe.sealy@hotmail.co.uk"

    results = soup.find_all("li", class_ = "s-item s-item__pl-on-bottom s-item--watch-at-corner", limit = 2)
    for products in results:

        title = products.find("h3", class_ ="s-item__title").text
        condition = products.find("span", class_ = "SECONDARY_INFO").text
        sellingPrice = products.find("span", class_ = "s-item__price").text
        timeLeft = products.find("span", class_ = "s-item__time-left")
        bids = products.find("span", class_ = "s-item__bids s-item__bidCount")
        buyItNow = products.find("span", class_ = "s-item__purchase-options-with-icon")
        link = products.find("a", class_ = "s-item__link")["href"]
        imgLink = products.find("img", class_ = "s-item__image-img")["src"]

        first_char = condition[0]
        if(first_char == "O"):
            condition = "Opened But Never Used"
        elif(first_char == "P"):
            condition = "Pre owned"  

        sellingTemp = sellingPrice.split("£")
        sellingPrice = (sellingTemp[1] + " Pounds")

        if buyItNow == None:
            buyItNow = "NaN"
            bids = bids.text
            timeLeft = timeLeft.text
        else:
            buyItNow = "Yes"
            bids = "NaN"
            timeLeft = "NaN"

    
        productFeatureList.append(f"Title: {title}\nCondition: {condition}\n"
        f"Selling Price: {sellingPrice}\nTime Left: {timeLeft}\n"
        f"Bids: {bids}\nBuy it Now?: {buyItNow}\nLink: {link}\n")
        
        image = imgEmbed(imgLink)
        imageList.append(image)

    msg.set_content(productFeatureList)

    for image in imageList:
        with open(image, "rb") as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
        msg.add_attachment(file_data, maintype = "image", subtype = file_type, filename = file_name)

    return msg

def imgEmbed(img):
    filename = img.split("/")[6] + ".jpg"
    r = requests.get(img, stream = True)
    
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

    return filename 

def send_mail(msg):

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADD, EMAIL_PASS)
        smtp.send_message(msg)
        print("mail has been sent")
        smtp.quit()


#while(True):
#    check_price()
#   time.sleep(60)

data = data_get(URL)
msg = data_find(data)
send_mail(msg)