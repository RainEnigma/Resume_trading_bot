from config import config

balance = config.kuna().fetch_balance()


class WorkCurrency():

    def __init__(self, name):
        self.name = name

    def now_curse(self):
        grn = balance.get(self.name).get("free")
        return grn

    def can_buy(self):
        cbn = balance.get(self.name).get("free")
        sell_now = config.kuna().fetch_ticker("WAVES/UAH").get("ask")  # сейчас продают
        in_waves_sans_comission = cbn/sell_now*0.995
        return in_waves_sans_comission
