from functions import animatedPrint as ap
from time import sleep
import datetime as dt
from PIL import Image as img


dig_size = 100

offsetx = 50
offsety = 50

dateOffset = -40
dateSpacing = -10

digits = img.open("three.jpg")
digits.convert("RGBA")
digits.thumbnail((dig_size,dig_size))
digits.save("digits.png", "PNG")

elements = {"0": None,
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,
            "7": None,
            "8": None,
            "9": None,
            "/": None
            }



def threshold(image,thres):
    pix = image.load()
    w, h = image.size
    for x in range(w):
        for y in range(h):
            if pix[x,y][0] > thres and pix[x,y][1] > thres and pix[x,y][2] > thres:
                pix[x,y] = (0,0,0,0)

def keepBlack(image):
    pix = image.load()
    w, h = image.size
    for x in range(w):
        for y in range(h):
            if pix[x, y][0] != 0 or pix[x, y][1] != 0 or pix[x, y][2] != 0:
                pix[x, y] = (255, 255, 255, 0)


def initializeDigits():
    global elements
    global dig_size

    for i in range(0, 10):
        digit = img.open("digits/"+str(i)+".png")
        digit.convert("RGBA")
        digit.thumbnail((dig_size, dig_size))
        keepBlack(digit)
        elements[str(i)] = digit

    slash = img.open("digits/slash.png")
    slash.convert("RGBA")
    keepBlack(slash)
    slash.thumbnail((dig_size, dig_size))
    elements['/'] = slash


def insertDate(main, new, offset, spacing):
    ap("\nInserting Date...")

    global elements
    global dig_size

    new_w, new_h = new.size

    new.paste(main)
    h = new_h // 2
    w = new_w // 2 + offset

    ap("\nGetting Date...")
    now = dt.datetime.now()
    full = str(now.date()).split("-")

    day = full[2]
    month = full[1]
    year = full[0]

    stringDate = day + "/" + month + "/" + year

    ap("\nBurning on the image...\n")
    for c in stringDate:
        curr = elements[c]
        new.paste(curr, (w,h))
        w += dig_size + spacing

#initializeDigits()

ap("Loading main image\n")

main = img.open("sign WhiteBG.jpg")

main = main.convert("RGBA")

main_w, main_h = main.size

keepBlack(main)

new = img.new("RGBA", (main_w * 3 //2, main_h ))

insertDate(main, new, dateOffset, dateSpacing)

new.save("test.png", "PNG")





