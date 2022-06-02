import imports

EMAIL_ADD = imports.Personal.EMAIL_ADDRESS
EMAIL_PASS = imports.Personal.EMAIL_PASSWORD
HEADER = imports.Personal.HEADER


URL = imports.URLs_productElements


class SenchFrontEnd:
    def __init__(self, app):
        self.item_text = imports.StringVar()
        self.item_Sites = ("","All","Amazon","Ebay","Etsy","Facebook","Gumtree" )
        self.option_var = imports.StringVar()
        self.option_var.set("Select an Option")



        self.app_Widgets(app)
        

    def app_Widgets(self, app):
        
        paddings = {"padx": 5, "pady": 5}

        #label next to search bar
        self.item_Search_Bar_Label = imports.Label(app, text = "Item:", background="#345", foreground="#fff")
        self.item_Search_Bar_Label.grid(row=0, column=0, sticky=imports.W, pady=20)
        #search bar string input
        self.item_entry = imports.Entry(app, textvariable = self.item_text)
        self.item_entry.grid(row=0,column=1, sticky=imports.W, **paddings)
        #drop down bar 
        self.drop_down_site = imports.OptionMenu(app, self.option_var, *self.item_Sites)
        self.drop_down_site.grid(row=0 , column=2, columnspan = 2, sticky=imports.W, **paddings)
        #item number label
        self.number_items_Label = imports.Label(app, text = "Amount of products:", background="#345", foreground="#fff")
        self.number_items_Label.grid(row=1, column=0, sticky=imports.W, pady=20)
        #spinbox how many products
        self.number_items = imports.Spinbox(app, width = 4, from_ = 0, to = 10)
        self.number_items.grid(row=1, column=1, **paddings)
        #Every(in mins)
        self.every_minutes_Label = imports.Label(app, text = "Every (in mins)", background="#345", foreground="#fff")
        self.every_minutes_Label.grid(row=2, column=0, sticky=imports.W, pady=20)
        #everysooften
        self.every_minutes = imports.Spinbox(app, width = 4, from_ = 0, to = 60)
        self.every_minutes.grid(row=2, column=1, **paddings)
        #runs for label
        self.runs_for_Label = imports.Label(app, text = "How long (in hrs)", background="#345", foreground="#fff")
        self.runs_for_Label.grid(row=3, column=0, sticky=imports.W, pady=20)
        #how long program run for
        self.runs_for = imports.Spinbox(app, width = 4, from_ = 0, to = 60)
        self.runs_for.grid(row=3, column=1, **paddings)
        #search button
        self.search_button = imports.Button(app, text = "Send", width = 6, command = self.item_option_get)
        self.search_button.grid(row=4, column=1, pady=20)
        #loading bar  
        self.progress_Bar = imports.Progressbar(app, orient=imports.HORIZONTAL, length=150, mode='determinate')
        self.progress_Bar.grid(row=5, column=0, columnspan=2)
        #loading bar percentage
        self.percentage_text = imports.Label(app,background = "#345",foreground = "#fff")
        self.percentage_text.grid(row=5, column=2, **paddings)
        #email conformation
        self.email_text = imports.Label(app,text ="", background = "#345", foreground = "RED", )
        self.email_text.grid(row=6,column = 0,columnspan=3, **paddings)


    def progress_Bar(self):
        pass

    def item_option_get(self, *args):
        if(self.number_items.get() == "" or self.item_entry.get() == "" or self.every_minutes.get() == "" or self.runs_for.get() == "" or self.option_var.get() =="Select an Option"):
            self.email_text["text"] = f"""You Must fill in all fields"""
        else:
            SenchGetSoup.data_find(SenchGetSoup, self.option_var.get(), self.item_text.get(), self.number_items.get())




            #self.email_text["text"] = f"""You will get {self.number_items.get()} {self.item_entry.get()} every {self.every_minutes.get()} Minutes for {self.runs_for.get()} hours from {self.option_var.get()}"""
            
            #for i in range(5):
           #     app.update_idletasks()
           #     self.progress_Bar ["value"] += 20
           #     imports.time.sleep(1)
            #    self.percentage_text["text"]=self.progress_Bar["value"],"%"

    

    def clearWidgets(self, app):
        for widgets in app.winfo_children():
            widgets.destroy()


class SenchGetSoup:
    def __init__(self)-> None:
        pass

    def data_find(self, key, item, AoP):
        AoP = int(AoP)
        itemNew = self.itemStringCheck(item)
        url = self.URLDictionary(key) + itemNew
        request = imports.requests.get(url, headers = HEADER)
        soup = imports.BeautifulSoup(request.text, "html.parser")
        SenchSiteScrape.filterOutData(SenchSiteScrape, key, soup, AoP)
        


    def URLDictionary(key):
        switch = {  
            "All":"""https://www.ebay.co.uk/sch/-
                     https://www.amazon.co.uk/s?k=-
                     https://www.facebook.com/marketplace/search/?query=-
                     https://www.gumtree.com/search?search_category=all&q=-
                     https://www.etsy.com/uk/search?q=""",

            "Ebay": "https://www.ebay.co.uk/sch/" , 
            "Amazon": "https://www.amazon.co.uk/s?k=", #think amazon double refreshes to prevent scrapping
            "Facebook": "https://www.facebook.com/marketplace/search/?query=",
            "Gumtree": "https://www.gumtree.com/search?search_category=all&q=", #%20 inbetween spaces
            "Etsy": "https://www.etsy.com/uk/search?q=",  
            "Shopify": " "                                                       #shopify 14 day free trail
        }
        return switch[key]
    def itemStringCheck(item):
        itemNew = item.replace(" ", "+")
        return itemNew

class SenchSiteScrape:
    def __init__(self) -> None:
        self.productNo = 0

    def filterOutData(self, key, soup, AoP):
        if key == "Ebay":
            ddItemList, imageList = self.EbayProductData(self, soup, AoP)

        if(key == "Amazon"):
            ddItemList, imageList = self.AmazonProductData(self, soup, AoP)
        
        if(key == "Facebook"):
           ddItemList, imageList = self.facebookProductData(self, soup, AoP)

        if(key == "Etsy"): 
           ddItemList, imageList = self.etsyProductData(self, soup, AoP)                        
        
        ddItemList = self.NoneError(ddItemList)
        imageList  = self.imgDownload(imageList)

        msgRoot = self.makingEmail(ddItemList, imageList)
        senchEmail.send(senchEmail, msgRoot, imageList)
        

    def EbayProductData(self, soup, AoP):
        imageList = []
        x = 0
        ddItemList = [[]]*AoP
        results = soup.find_all("li", class_ = "s-item s-item__pl-on-bottom s-item--watch-at-corner", limit = AoP )
        for products in results:
            divlist = []
            priceList = products.find_all("div", class_ = "s-item__detail s-item__detail--primary")

            for prices in priceList:
                divlist.append(prices.find("span", class_ ="s-item__price"))

            sellingPrice = divlist[0]
            buyItNowPrice = divlist[2]


            title = products.find("h3", class_ ="s-item__title")
            condition = products.find("span", class_ = "SECONDARY_INFO")
            timeLeft = products.find("span", class_ = "s-item__time-left")
            bids = products.find("span", class_ = "s-item__bids s-item__bidCount")
            buyItNowNoNum = products.find("span", class_ = "s-item__purchase-options-with-icon")
            link = products.find("a", class_ = "s-item__link")["href"].split("?")[0]
            imgLink = products.find("img", class_ = "s-item__image-img")["src"]

            ddItemList[x] = [title,condition,sellingPrice,timeLeft,bids,buyItNowPrice,link]
            imageList.append(imgLink)

            x+=1

        return ddItemList,imageList

    def AmazonProductData(self, soup, AoP):
            imageList = []
            x = 0
            ddItemList = [[]]*AoP
            print(soup)
            results = soup.find("span",class_ = "a-size-medium a-color-base a-text-normal")
            #use API FOR AMAZON
            # for products in results:
            #     title = products.find("span", class_ = "a-size-medium a-color-base a-text-normal")
            #     print (title) 
            #     review = products.find("li", class_ = "a-icon a-icon-star-small a-star-small-4 aok-align-bottom").find("span", "a-icon a-icon-star-small a-star-small-4 aok-align-bottom")
            #     amountofreview = products.find("span", class_ ="a-size-base s-underline-text")
            #     priceWhole = products.find("span", class_ = "a-price-whole")
            #     pricePence = products.find("span", class_ = "a-price-fraction")
            #     dateRecievedBy = products.find("span", class_ = "a-text-bold")
            #     if(products.find("span", class_ = "a-icon a-icon-prime a-icon-medium")):
            #         primeBool = "Yes"
            #     else:
            #         primeBool = "No"
            #     link = products.find("a", "a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"].split("?")[0]
            #     imgLink = products.find("img","s-image")["src"]

    def facebookProductData(self, soup, AoP):
        imageList = []
        x = 0
        ddItemList = [[]]*AoP
        print(soup)
        results = soup.find("span",class_ = "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7")
        print(results)
        
        #Use the Facebook API
    
    def etsyProductData(self, soup, AoP):
        imageList = []
        x = 0
        ddItemList = [[]]*AoP
        results = soup.find_all("li",class_ = "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 wt-order-xs-0 wt-order-md-0 wt-order-lg-0 wt-show-xs wt-show-md wt-show-lg", limit = AoP)
        for products in results:
            title = products.find("div", class_=" ").find("h3", )
            stars = products.find("span", class_ = "screen-reader-only")
            aOReviews = products.find("span", class_ = "wt-text-body-01 wt-nudge-b-1 wt-text-gray wt-display-inline-block")
            price = products.find("span", class_ = "currency-value")
            starSeller = products.find("div", class_ = "wt-nudge-b-1 wt-display-inline-flex-xs wt-flex-nowrap wt-align-items-center")
            discount = products.find("p", class_ = "wt-text-caption search-collage-promotion-price wt-text-slimewt-text-truncate wt-no-wrap")
            delivery = products.find("div", class_ = "wt-badge wt-badge--small wt-badge--sale-01")
            #image = products.find("img", class_ = "data-listing-card-listing-image")["src"]
            #link = products.find("a", class_ = "listing-link wt-display-inline-block5494d36ddec45237logged")["href"].split("?")[0]
            print(title)
            




    def NoneError(List):
        for x in range(len(List)):
            for y in range(len(List[x])):
                if List[x][y] == None:
                    List[x][y] = "NaN"
                elif type(List[x][y]) != str:
                    List[x][y]  = List[x][y].text
        return List

    def imgDownload(imageList):
        for i in range(len(imageList)):
            r = imports.requests.get(imageList[i], stream = True)
            imageList[i] = imageList[i].split("/")[6] + str(i) + ".jpg"
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(imageList[i],'wb') as f:
                    imports.shutil.copyfileobj(r.raw, f)
                print('Image sucessfully Downloaded: ',imageList[i])
            else:
                print('Image Couldn\'t be retreived')

        return imageList
    def makingEmail(ddItemList, imageList):

        imports.msgRoot = imports.MIMEMultipart('related')
        imports.msgRoot['Subject'] = 'poo boy heres some cards'
        imports.msgRoot['From'] = EMAIL_ADD
        imports.msgRoot['To'] = "Joe.sealy@hotmail.co.uk"
        imports.msgRoot.preamble = 'Multi-part message in MIME format.'
        msgAlternative = imports.MIMEMultipart('alternative')
        imports.msgRoot.attach(msgAlternative)
        i=0
        html_List =""
        for x in range(len(ddItemList)):
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
            </p>""".format(i = i, title = ddItemList[x][0], condition = ddItemList[x][1], sellingPrice = ddItemList[x][2], timeLeft = ddItemList[x][3], bids = ddItemList[x][4], buyItNowPrice = ddItemList[x][5], link = ddItemList[x][6])

            with open (imageList[x], 'rb') as img:
                msg_img = imports.MIMEImage(img.read())
                msg_img.add_header('Content-ID', '<image'+str(i)+'>')
                imports.msgRoot.attach(msg_img)
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

        msgAlternative.attach(imports.MIMEText(html_Full , "html"))
        msgRoot = imports.msgRoot.as_string()
        return msgRoot



class senchEmail:
    def __init__(self) -> None:
        pass


    def send(self, msg, imageListFull):
        smtp = imports.smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADD, EMAIL_PASS)
        smtp.sendmail(EMAIL_ADD, "Joe.Sealy@hotmail.co.uk", msg)
        print("mail has been sent")
        smtp.quit()

        for image in imageListFull:
            imports.os.remove(image)

if __name__ == "__main__":
    app = imports.Tk()
    SenchFrontEnd(app)
    app.geometry("400x400")
    app.title("Sench")
    app.config(bg='#345')
    app.mainloop()