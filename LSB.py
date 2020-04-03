import binascii
import time
import math
from PIL import Image, ImageFilter, ImageDraw
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageFilter, ImageDraw
from PIL.ImageQt import ImageQt

image = "stego-output.bmp"
input = open("notes.txt", 'rb')
byte_list = []
byte = input.read(1)
while byte:
    byte_list.append(byte)
    byte = input.read(1)
input.close()

# Define functions
def makeEven(input):
    return (input % 2) + input - ((input % 2) * 2)

def makeOdd(input):
    return (input % 2 + 1) + input - ((input % 2) * 2)

def oddWhiteEvenBlack(input):
    if input % 2 == 1:
        return 255
    else:
        return 0

def encode(self, imagePath, byte_list):
    # Make sure there's actually files
    if imagePath == "" or len(byte_list) <= 0:
        return

    # Define Variables
    img = Image.open(imagePath)

    # Turn the bytes into binary
    bits = []
    for i in byte_list:
        byteNum = int(int.from_bytes(i, byteorder='big'))
        for power in range(7, -1, -1):
            num = byteNum / math.pow(2,power)
            byteNum %= math.pow(2,power)
            bits.append(int(num))

    pixelCount = img.size[0] * img.size[1] * 3
    if len(bits) > pixelCount:
        QMessageBox.critical(self, "Error", "Your selected file is too big to encrypt in your selected image. Select a different file or image.", QMessageBox.Ok)
        return None


    print("File Read Complete.")
    # Encode image
    encodestart = time.time()
    print("Encoding Image...")
    # Create the masks
    maskR = Image.new('L', img.size, 'black')
    maskG = Image.new('L', img.size, 'black')
    maskB = Image.new('L', img.size, 'black')
    masks = [maskR, maskG, maskB]

    mwidth = self.maskDisplay.pixmap().width()
    mheight = self.maskDisplay.pixmap().height()
    pixmap = pixMap = QPixmap.fromImage(QImage(mwidth, mheight, QImage.Format_ARGB32))
    self.maskDisplay.setPixmap(pixmap)
    ratio = mwidth / img.size[0]
    if ratio < 1:
        ratio = 1
    width = img.size[0]
    height = img.size[1]
    painter = QPainter(self.maskDisplay.pixmap())
    curChn = 0
    print(self.palette().color(QPalette.Window))
    print(self.palette().color(QPalette.Window).getRgb())
    for num in range(len(bits)):
        chn = int(num / (width * height))
        x = int((num / height) - (width * chn))
        y = (num % height)
        if curChn != chn:
            painter.setPen(self.palette().color(QPalette.Window))
            painter.fillRect(0, 0, mwidth, mheight, self.palette().color(QPalette.Window))
            self.maskDisplay.update()
            curChn = chn
        if bits[num] == 1:
            masks[chn].putpixel((x,y), 255)
            painter.setPen(QColor(255,255,255))
            painter.drawRect(x*ratio, y*ratio, ratio, ratio)
        else:
            masks[chn].putpixel((x,y), 0)
            painter.setPen(QColor(0,0,0))
            painter.drawRect(x*ratio, y*ratio, ratio, ratio)
        self.maskDisplay.update()
        self.progressBar.setProperty("value", ((num+1)/len(bits))*95)

    print("Making Encoded Image...")
    # Change the channels
    if img.mode == "ARGB":
        a, r, g, b = img.split()
    else:
        r, g, b = img.split()
    nr, ng, nb = r, g, b

    r = r.point(makeEven)
    nr = r.point(makeOdd)
    r.paste(nr, None, masks[0])

    g = g.point(makeEven)
    ng = g.point(makeOdd)
    g.paste(ng, None, masks[1])

    b = b.point(makeEven)
    nb = b.point(makeOdd)
    b.paste(nb, None, masks[2])

    # Save it
    img = Image.merge("RGB", (r, g, b))

    encodeend = time.time()
    encodetime = encodeend - encodestart
    print("Image Encoded in " + str(round(encodetime,2)) + " seconds.")
    self.progressBar.setProperty("value", 100)
    #self.label_2.setText("Complete")

    return ImageQt(img)

def decode(self, imagePath):
#def decode(imagePath):
    decodestart = time.time()
    print("Reading Raw Binary...")
    img = Image.open(imagePath)
    r,g,b = img.split()
    r = r.point(oddWhiteEvenBlack)
    g = g.point(oddWhiteEvenBlack)
    b = b.point(oddWhiteEvenBlack)
    masks = [r, g, b]
    rawBinary = ""

    width = img.size[0]
    height = img.size[1]
    pixelCount = width*height*3
    for num in range(pixelCount):
        chn = int(num / (width * height))
        x = int((num / height) - (width * chn))
        y = (num % height)
        if masks[chn].getpixel((x,y)) % 2 == 1:
            rawBinary += "1"
        else:
            rawBinary += "0"
        self.progressBar.setProperty("value", ((num+1)/pixelCount)*95)

    print("Splitting Raw Binary into Bytes...")
    count = 0
    rawBinaryList = list()
    for num in range(int(len(rawBinary)/8)):
        rawBinaryList.append(int(rawBinary[count:count+8],2))
        count += 8
    self.progressBar.setProperty("value", 100)
    print("Process Completed.")

    return rawBinaryList
