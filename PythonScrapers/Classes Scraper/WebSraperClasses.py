from tkinter import Variable

from sqlalchemy import values
import imports

EMAIL_ADD = imports.Personal.EMAIL_ADDRESS
EMAIL_PASS = imports.Personal.EMAIL_PASSWORD
HEADER = imports.Personal.HEADER


URL = imports.URLs_productElements


class InfoScraperFrontEnd:
    def __init__(self, app):
        self.item_text = imports.StringVar()
        self.item_Sites = ("All","Amazon","Ebay","Etsy","Facebook","Gumtree" )
        self.option_var = imports.StringVar()
        self.option_var.set("Select an Option")



        self.app_Widgets(app)
        

    def app_Widgets(self, app):
        
        paddings = {"padx": 5, "pady": 5}

        #label next to search bar
        item_Search_Bar_Label = imports.Label(app, text = "Item:", font = ("Bold", 10), pady = 20)
        item_Search_Bar_Label.grid(row=0, column=0, sticky=imports.W)

        #search bar string input
        item_entry = imports.Entry(app, textvariable = self.item_text)
        item_entry.grid(row=0,column=1, sticky=imports.W, **paddings)

        #drop down bar 
        drop_down_site = imports.OptionMenu(app, self.option_var, *self.item_Sites, command=self.option_changed )
        drop_down_site.grid(row=0 , column=2, sticky=imports.W, **paddings)

        self.output_selection_label = imports.Label(app, foreground='red')
        self.output_selection_label.grid(row=1, column=0, columnspan=2, sticky=imports.W, **paddings)
                                      
    def option_changed(self):
        self.output_selection_label['text'] = f'You selected: {self.option_var.get()}'

    def clearWidgets(self, app):
        for widgets in app.winfo_children():
            widgets.destroy()

class infoScraperBackEnd:
    def __init__(self)-> None:
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        'From': 'joe.sealy@hotmail.co.uk' 
        }


        pass

    def URLDictionary(key):
        switch = {  
            "Ebay": "https://www.ebay.co.uk/sch/" , 
            "Amazon": "https://www.amazon.co.uk/s?k=", #think amazon double refreshes to prevent scrapping
            "Facebook": "https://www.facebook.com/marketplace/search/?query=",
            "Gumtree": "https://www.gumtree.com/search?search_category=all&q=", #%20 inbetween spaces
            "Etsy": "https://www.etsy.com/uk/search?q=",  
            "Shopify": " "                                                       #shopify 14 day free trail
        }
        return switch[key]

    def 

    


if __name__ == "__main__":
    app = imports.Tk()
    InfoScraperFrontEnd(app)
    app.geometry("400x200")
    app.title("Sench")
    app.mainloop()