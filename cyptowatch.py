import requests
import json
import ctypes
import shutil
import os.path
import os
from PIL import Image, ImageDraw, ImageFont

apikey = ""
currencies = ["BAT", "VET", "BTC", "ETH", "LUNA", "XVS", "XRP", "LINK", "ADA"]
curs = []


class currency:
    r = None
    price = None
    inc = None
    symbol = None
    json = None
    text = None

    def __init__(self, symbol, resp):
        self.text = []
        self.price = resp["data"][symbol]["quote"]["USD"]["price"]
        self.inc = resp["data"][symbol]["quote"]["USD"]["percent_change_24h"]
        self.text.append(f"PRC ({symbol}): {round(self.price, 2)}")
        self.text.append(f"INC: {round(self.inc,2)}%")


url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol="
url += currencies.__repr__().replace("'", "").replace(" ", "")[1:-1]
# for a in currencies:
#    url += a+","

r = requests.get(
    url, headers={"X-CMC_PRO_API_KEY": apikey})
resp = json.loads(r.text)

for a in currencies:
    curs.append(currency(a, resp))

path = os.environ["LOCALAPPDATA"]+"\\original.png"

if not os.path.isfile(path):
    shutil.copy2(os.environ["APPDATA"]+"\\Microsoft\\Windows\\"
                 "Themes\\CachedFiles\\CachedImage_1920_1080_POS4.jpg", path)

base = Image.open(path).convert("RGBA")
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
fnt = ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 18)
d = ImageDraw.Draw(txt)
for c in range(len(curs)):
    d.text((1740, 1014-c*60), curs[c].text[0],
           font=fnt, fill=(255, 255, 255, 255))
    d.text((1740, 1044-c*60), curs[c].text[1], font=fnt,
           fill=(255, 255, 255, 255))
out = Image.alpha_composite(base, txt)
out.save(os.environ["LOCALAPPDATA"]+"\\Temp\\back.png")
ctypes.windll.user32.SystemParametersInfoW(0x14, 0, (
                                           os.environ["LOCALAPPDATA"] +
                                           "\\Temp\\back.png"), 0)
