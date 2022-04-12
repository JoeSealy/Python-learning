from cgitb import html
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
    productElement = []
    imageList = []
    image_cid = []
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Test HTML Email"
    msg['From'] = EMAIL_ADD
    msg['To'] = "joe.sealy@hotmail.co.uk"

    #msg = EmailMessage()
    #msg['Subject'] = "Some Cards poo boy"
    #msg.set_content("")
    
    
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
        title = asciiErrorCheck(title)
        condition = asciiErrorCheck(condition)
        sellingPrice = asciiErrorCheck(sellingPrice)
        timeLeft,bids,buyItNow = NaNObjects(timeLeft,bids,buyItNow)
        linkShort = link.split("?")[0]

        productElement.extend([image, title, condition, sellingPrice, timeLeft, bids, buyItNow, linkShort])
        imageList.append(image)

    forEnd = len(productElement)
    for i in range(0, forEnd, 8):
        image_cid[i] = make_msgid()

    html_template = """\
    <html>
        <body>
        {% for element in range(0, forEnd, 8) %}
        <p>
            <img src="cid:{{image_cid[element]}}"align="right">
            <span style="font-size: 20px;">Title:</span><span style="font-size: 15px;"> {{productElement[element + 1]}}</span><br>
            <span style="font-size: 20px;">Condition:</span><span style="font-size: 15px;"> {{productElement[element + 2]}}</span><br>
            <span style="font-size: 20px;">Selling Price:</span><span style="font-size: 15px;">  {{productElement[element+ 3]}}</span><br>
            <span style="font-size: 20px;">Time Left:</span><span style="font-size: 15px;">  {{productElement[element + 4]}}</span><br>
            <span style="font-size: 20px;">Bids:</span><span style="font-size: 15px;"> {{productElement[element + 5]}}</span><br>
            <span style="font-size: 20px;">Buy it Now?:</span><span style="font-size: 15px;">  {{productElement[element + 6]}}</span><br>
            <span style="font-size: 20px;">Link:</span><span style="font-size: 15px;"> {{productElement[element + 7]}}</span><br>
        </p>
        {% endfor %}
        </body>
    </html>  
    """
    for i in range(0, forEnd, 8):
        with open(productElement[i], 'rb') as img:
            maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')
            msg.get_payload()[1].add_related(img.read(),maintype=maintype,subtype=subtype,cid=image_cid[i])

    template = Environment(loader=BaseLoader).from_string(html_template)
    template_vars = {"forEnd": forEnd, "productElement": productElement, "image_cid": image_cid[1:-1], }
    html_out = template.render(template_vars)

    part2 = MIMEText(html_out, 'html')
    msg.attach(part2)
    msg = msg.as_string()
    return msg, imageList

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