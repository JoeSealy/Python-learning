

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




