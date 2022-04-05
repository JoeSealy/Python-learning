import imghdr
import requests
import pandas as pd
import smtplib
import time
import base64 
import os
import personal
import shutil 
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

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
        image = imgEmbed(imgLink)
        #imageList.append(image)

        title = asciiErrorCheck(title)
        condition = asciiErrorCheck(condition)
        sellingPrice = asciiErrorCheck(sellingPrice)

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
        f"Bids: {bids}\nBuy it Now?: {buyItNow}\nLink: {link}\n"
        f"________________________________________________________________________________________________________\n\n")


    msg = productFeatureList
    msg = concat(msg)
    subject = "Some Gcards poo boy"
    message = f"Subject:{subject}\n\n{msg}".format(subject, msg)

    return message, imageList

def asciiErrorCheck(text):
    asciiErrorFree = []
    fixedText = ""
    asciiCharList = list(text)
    for char in asciiCharList:
        check_ascii_char = char.isascii()
        if check_ascii_char == False:
            char = ""
        asciiErrorFree.append(char)
    
    for x in asciiErrorFree:
        fixedText+=x

    return fixedText

def concat(stringList):
    body = ""
    for string in stringList:
        body += string
    return body

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

def send_mail(msg, imageList):

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_ADD, EMAIL_PASS)
    subject = "Some Gcards poo boy"
    message = f"Subject:{subject}\n\n{msg}".format(subject, msg)
    smtp.sendmail(EMAIL_ADD, "joe.sealy@hotmail.co.uk", message)
    print("mail has been sent")
    smtp.quit()

    for image in imageList:
        os.remove(image)


#while(True):
#    check_price()
#   time.sleep(60)

if __name__ == "__main__":
    data = data_get(URL)
    msg, imageList = data_find(data)
    send_mail(msg, imageList)