from functions import animatedPrint as ap
from time import sleep



from PIL import Image as img


def keepBlack(image, w, h):
    pix = image.load()
    for x in range(w):
        for y in range(h):
            if pix[x, y] != (0, 0, 0, 255):
                pix[x, y] = (0, 0, 0, 0)

def threshold(image, w, h, threshold):
    pix = image.load()
    for x in range(w):
        for y in range(h):
            if pix[x,y][0] > thres and pix[x,y][1] > thres and pix[x,y][2] > thres:
                pix[x,y] = (0,0,0,0)



mode = int(input("Select mode: \n 1.Delete colors above threshold \n 2.Keep only black \n : "))
if mode == 1:
    thres = int(input("\nThreshold: "))
elif mode != 2:
    print("Enter 1 or 2 for the modes.")
    sleep(3)
    exit()

name = input("Enter name to be saved with: ")

ap("Loading 'sign WhiteBG.jpg'\n")

im = img.open("sign WhiteBG.jpg")

im = im.convert("RGBA")

dig = img.open("digit.jpg")

w, h = im.size

#new size
w_, h_ = w*2, h


ap("\nProcessing...\n")

if mode == 1:
    threshold(im, w, h, thres)
else:
    keepBlack(im, w, h)

width, height = im.size

ap("\nSaving...\n")

im.save("{}.png".format(name), "PNG")

ap("\nCompleted!\n")

input("Press any key to continue.")


