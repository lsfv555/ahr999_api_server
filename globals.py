# globals.py

class Subscription:
    def __init__(self, url, enable_quote_notif, quote_threshold):
        self.url = url
        self.enable_quote_notif = enable_quote_notif
        self.quote_threshold = quote_threshold

    def to_dict(self):
        return {
            "url": self.url,
            "enable_quote_notif": self.enable_quote_notif,
            "quote_threshold": self.quote_threshold
        }

url_data = {
    "title": "Successfully obtain data！",
    "text": "",
    "icon": "https://en.bitcoin.it/w/images/en/2/29/BC_Logo_.png"
}

price_change_data = {
    "title": "Price change！",
    "text": "",
    "icon": "https://en.bitcoin.it/w/images/en/2/29/BC_Logo_.png"
}

full_data = {
    "ahr999": "",
    "update_time": "",
    "unix_time": "",
    "price": "",
    "cost_200day": "",
    "exp_growth_valuation": ""
}

subscriptions = []
