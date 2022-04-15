from cgitb import html, reset
import imghdr
import requests
import pandas as pd
import smtplib
import time
import base64 
import os
import personal
import shutil
import mimetypes
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.utils import make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from jinja2 import Environment, BaseLoader

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
    productElement = []
    html_list = []
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'test message'
    msgRoot['From'] = EMAIL_ADD
    msgRoot['To'] = "joe.sealy@hotmail.co.uk"
    msgRoot.preamble = 'Multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    html_List =""
    i = 0

    results = soup.find_all("li", class_ = "s-item s-item__pl-on-bottom s-item--watch-at-corner", limit = 5)

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
        title = asciiErrorCheck(title)
        condition = asciiErrorCheck(condition)
        sellingPrice = asciiErrorCheck(sellingPrice)
        timeLeft,bids,buyItNow = NaNObjects(timeLeft,bids,buyItNow)
        linkShort = link.split("?")[0]
        imageList.append(image)

        #image_cid = make_msgid()
        #productElement.extend([image, title, condition, sellingPrice, timeLeft, bids, buyItNow, linkShort])

        html="""
        <p>
            <img src="cid:image{i}"align="right">
            <span style="font-size: 20px;">Title:</span><span style="font-size: 15px;"> {title}</span><br>
            <span style="font-size: 20px;">Condition:</span><span style="font-size: 15px;"> {condition}</span><br>
            <span style="font-size: 20px;">Selling Price:</span><span style="font-size: 15px;">  {sellingPrice}</span><br>
            <span style="font-size: 20px;">Time Left:</span><span style="font-size: 15px;">  {timeLeft}</span><br>
            <span style="font-size: 20px;">Bids:</span><span style="font-size: 15px;"> {bids}</span><br>
            <span style="font-size: 20px;">Buy it Now?:</span><span style="font-size: 15px;">  {buyItNow}</span><br>
            <span style="font-size: 20px;">Link:</span><span style="font-size: 15px;"> {linkShort}</span><br>
        </p>""".format(i = i, title = title, condition = condition, sellingPrice = sellingPrice, timeLeft = timeLeft, bids = bids, buyItNow = buyItNow, linkShort = linkShort)

        with open (imageList[i], 'rb') as img:
            msg_img = MIMEImage(img.read())
            msg_img.add_header('Content-ID', '<image'+str(i)+'>')
            msgRoot.attach(msg_img)
            img.close()

        i += 1
        html_List += html


    html_Full = """ 
        <html>
            <body>
                {html_List}
            </body>
        </html>
    """.format(html_List = html_List)

    msgAlternative.attach(MIMEText(html_Full , "html"))
    msgRoot = msgRoot.as_string()
    #print(msg)
    return msgRoot, imageList

def NaNObjects(timeLeft,bids,buyItNow ):
    if timeLeft == None:
        timeLeft = "NaN"
    else:
        timeLeft = timeLeft.text

    if bids == None:
        bids = "NaN"
    else:
        bids = bids.text

    if buyItNow == None:
        buyItNow = "NaN"
    else:
        buyItNow = "Yes"
 

    return timeLeft,bids,buyItNow 

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
    smtp.ehlo()
    smtp.login(EMAIL_ADD, EMAIL_PASS)
    smtp.sendmail(EMAIL_ADD, "joe.sealy@hotmail.co.uk", msg)
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