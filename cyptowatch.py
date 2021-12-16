import requests
import json
import ctypes
import shutil
import os.path
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont


currencies = ["BAT", "VET", "BTC", "ETH", "LUNA", "XVS", "XRP", "LINK", "ADA"]
spacing = 5
margin = (5, 200)

if sys.argv[-1] != "-d":
    if subprocess.Popen("schtasks.exe /Query /TN CryptoWatch".split(), stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).wait():
        if ctypes.windll.shell32.IsUserAnAdmin():
            execpath = os.path.dirname(
                sys.executable) + "\\pythonw.exe " + __file__ + " -d"
            os.system(
                f"schtasks.exe /Create /SC ONLOGON /TN CryptoWatch /TR \"{execpath}\" /IT")
            os.system("echo.|schtasks.exe /Change /TN CryptoWatch /RI 5")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", os.path.dirname(
                sys.executable) + "\\python.exe", " ".join(sys.argv), None, 0)


class currency:
    def __init__(self, symbol: str, resp: dict):
        self.price: int = resp["data"][symbol]["quote"]["USD"]["price"]
        self.inc: int = resp["data"][symbol]["quote"]["USD"]["percent_change_24h"]
        self.text = f"{symbol}: {round(self.price, 2)} ({round(self.inc, 2)}%)"


res = (ctypes.windll.user32.GetSystemMetrics(0),
       ctypes.windll.user32.GetSystemMetrics(1))
curs: list[currency] = []

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol="
url += ",".join(currencies)

r = requests.get(
    url, headers={"X-CMC_PRO_API_KEY": "APIKEY"})
resp: dict = json.loads(r.text)

for a in currencies:
    curs.append(currency(a, resp))

path = os.environ["LOCALAPPDATA"]+"\\original.png"

if not os.path.isfile(path):
    shutil.copy2(os.environ["APPDATA"]+"\\Microsoft\\Windows\\"
                 "Themes\\CachedFiles\\CachedImage_1920_1080_POS4.jpg", path)

base = Image.open(path).convert("RGBA")
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
fnt = ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 19)
d = ImageDraw.Draw(txt)

for c in range(len(curs)):
    colour = (255, 255, 255, 255)

    if curs[c].inc > 0:
        colour = (22, 199, 132, 255)
    else:
        colour = (234, 57, 67, 255)
    size = d.textsize(curs[c].text, fnt)
    d.text((res[0]-margin[0]-size[0], res[1]-margin[1]-c*(size[1]+spacing)), curs[c].text, font=fnt,
           fill=colour)

out = Image.alpha_composite(base, txt)
out.save(os.environ["LOCALAPPDATA"]+"\\Temp\\back.png")
ctypes.windll.user32.SystemParametersInfoW(0x14, 0, (
                                           os.environ["LOCALAPPDATA"] +
                                           "\\Temp\\back.png"), 0)
