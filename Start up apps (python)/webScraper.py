from matplotlib import image
import requests
import pandas as pd
import smtplib
import time
import os
from sqlalchemy import true
import personal
import shutil
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage



EMAIL_ADD = personal.EMAIL_ADDRESS
EMAIL_PASS = personal.EMAIL_PASSWORD
HEADER = personal.HEADER

URL = "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=Palit+Jetstream+GeForce+GTX+1060+6GB&_sacat=0&LH_TitleDesc=0&_odkw=Palit+GeForce+GTX+1060+6GB&_osacat=0"

def data_get(URL):
    request = requests.get(URL, headers = HEADER)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup

def data_find(soup):
    imageList = []
    html_List =""
    i = 0


    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'poo boy heres some cards'
    msgRoot['From'] = EMAIL_ADD
    msgRoot['To'] = "Joe.sealy@hotmail.co.uk"
    msgRoot.preamble = 'Multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    

    results = soup.find_all("li", class_ = "s-item s-item__pl-on-bottom s-item--watch-at-corner", limit = 10)

    for products in results:
        divlist = []
        priceList = products.find_all("div", class_ = "s-item__detail s-item__detail--primary")

        for prices in priceList:
            divlist.append(prices.find("span", class_ ="s-item__price"))
            
        sellingPrice = NaNObjects(divlist[0])
        buyItNowPrice = NaNObjects(divlist[2])

        sellingPrice = asciiErrorCheck(sellingPrice)
        buyItNowPrice = asciiErrorCheck(buyItNowPrice)

        a = priceCheck(buyItNowPrice)
        b = priceCheck(sellingPrice)

        if a or b == True:  
            title = NaNObjects(products.find("h3", class_ ="s-item__title"))
            condition = NaNObjects(products.find("span", class_ = "SECONDARY_INFO"))
            timeLeft = NaNObjects(products.find("span", class_ = "s-item__time-left"))
            bids = NaNObjects(products.find("span", class_ = "s-item__bids s-item__bidCount"))
            buyItNowNoNum = NaNObjects(products.find("span", class_ = "s-item__purchase-options-with-icon"))
            link = products.find("a", class_ = "s-item__link")["href"].split("?")[0]
            imgLink = products.find("img", class_ = "s-item__image-img")["src"]

            title = asciiErrorCheck(title)
            condition = asciiErrorCheck(condition)

            if(buyItNowPrice == "NaN"):
                if(buyItNowNoNum != "NaN"):
                    buyItNowPrice = "Yes"

            html="""
            <p>
                <img src="cid:image{i}"align="right">
                <span style="font-size: 20px;">Title:</span><span style="font-size: 15px;"> {title}</span><br>
                <span style="font-size: 20px;">Condition:</span><span style="font-size: 15px;"> {condition}</span><br>
                <span style="font-size: 20px;">Selling Price:</span><span style="font-size: 15px;">  {sellingPrice}</span><br>
                <span style="font-size: 20px;">Time Left:</span><span style="font-size: 15px;">  {timeLeft}</span><br>
                <span style="font-size: 20px;">Bids:</span><span style="font-size: 15px;"> {bids}</span><br>
                <span style="font-size: 20px;">Buy it Now?:</span><span style="font-size: 15px;"> {buyItNowPrice}</span><br>
                <span style="font-size: 20px;">Link:</span><span style="font-size: 15px;"> {link}</span><br>
            </p>""".format(i = i, title = title, condition = condition, sellingPrice = sellingPrice, timeLeft = timeLeft, bids = bids, buyItNowPrice = buyItNowPrice, link = link)


            image, imageListFull = imgDownaload(imgLink,imageList,i)
            with open (image, 'rb') as img:
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
    return msgRoot, imageListFull

def priceCheck(a):
    a = float(a)
    print(a)
    if a < 150:
        return True
    else:
        return False
  
def NaNObjects(x):
    if x == None:
        x = "NaN"
    else:
        x = x.text

    return x 

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

def imgDownaload(img,imageList, i):
    filename = img.split("/")[6] + str(i) +".jpg"

    r = requests.get(img, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

    imageList.append(filename)    

    return filename, imageList 

def send_mail(msg, imageListFull):

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADD, EMAIL_PASS)
    smtp.sendmail(EMAIL_ADD, "Joe.Sealy@hotmail.co.uk", msg)
    print("mail has been sent")
    smtp.quit()

    for image in imageListFull:
        os.remove(image)


#while(True):
#    check_price()
#    time.sleep(60)

if __name__ == "__main__":
    data = data_get(URL)
    msg, imageListFull = data_find(data)
    send_mail(msg, imageListFull)