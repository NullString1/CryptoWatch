import requests
import lxml.html
import ctypes
import shutil
import os.path
import os
from PIL import Image, ImageDraw, ImageFont

curs = []


class cur:
    r = None
    data = None
    price = None
    inc = None
    name = None
    text = None
    style = None
    def __init__(self, url, name):
        self.text = []
        self.r = requests.get(url, headers={"content-encoding": "gzip"},
                              stream=True)
        self.r.raw.decode_content = True
        self.data = (lxml.html.parse(self.r.raw)
                     .xpath("//div[contains(@class, 'sc-16r8icm-0 kXPxnI"
                            " priceTitle___1cXUG')]/*"))
        self.price = "$" + str(round(float(self.data[0].text[1:]
                                           .replace(",", "")), 4))
        self.inc = self.data[1].text_content().replace("(",
                                                       "").replace(")", "")
        style = self.data[1].attrib.get("style")
        if style.find("up-color") == -1:
            self.inc = "-"+self.inc
        self.name = name
        self.text.append(f"PRC ({self.name}): {self.price[:8]}")
        self.text.append(f"INC: {self.inc}")


curs.append(cur("https://coinmarketcap.com/currencies/basic-attention-token",
                "BAT"))
curs.append(cur("https://coinmarketcap.com/currencies/monero", "XMR"))
curs.append(cur("https://coinmarketcap.com/currencies/ethereum", "ETH"))
curs.append(cur("https://coinmarketcap.com/currencies/bitcoin", "BTC"))

path = os.environ["LOCALAPPDATA"]+"\\original.png"

if not os.path.isfile(path):
    shutil.copy2(os.environ["APPDATA"]+"\\Microsoft\\Windows\\"
                 "Themes\\CachedFiles\\CachedImage_1920_1080_POS4.jpg", path)

base = Image.open(path).convert("RGBA")
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
fnt = ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 18)
d = ImageDraw.Draw(txt)
for c in range(len(curs)):
    d.text((1740, 954-c*60), curs[c].text[0],
           font=fnt, fill=(255, 255, 255, 255))
    d.text((1740, 984-c*60), curs[c].text[1], font=fnt,
           fill=(255, 255, 255, 255))
out = Image.alpha_composite(base, txt)
out.save(os.environ["LOCALAPPDATA"]+"\\Temp\\back.png")
ctypes.windll.user32.SystemParametersInfoW(0x14, 0, (
                                           os.environ["LOCALAPPDATA"] +
                                           "\\Temp\\back.png"), 0)
