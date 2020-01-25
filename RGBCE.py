import binascii
import time
from PIL import Image, ImageFilter, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImageReader, QImage, QPixmap, QPainter
from PIL import Image, ImageFilter, ImageDraw
from PIL.ImageQt import ImageQt

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

def encode(self, imagePath, filePath):
    #img = Image.new('RGB', (200,300), 'black')

    # Make sure there's actually files
    if imagePath == "" or filePath == "":
        return

    # Define Variables
    img = Image.open(imagePath)
    
    file = open(filePath, 'rb')

    print("Reading Source File...")
    # Read the hex of the file
    byte_list = bytearray()
    byte = file.read(1)
    while byte:
        byte_list += bytes(byte)
        byte = file.read(1)

    # Turn the bytes into BINARY
    codestr = ""
    for i in byte_list:
        codestr += format(i, '08b')
    print("File Read Complete.")
    # Encode image
    encodestart = time.time()
    print("Encoding Image...")
    # Create the masks
    maskR = Image.new('L', img.size, 'black')
    maskG = Image.new('L', img.size, 'black')
    maskB = Image.new('L', img.size, 'black')

    count = 0
    self.label_2.setText("Encoding Data...")
    print("Encoding Red Channel...")
    while count <= img.size[0] * img.size[1] and count < len(codestr):
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                self.progressBar.setProperty("value", ( count / len(codestr) ) * 100)
                if codestr[count:count+1] == "1":
                    maskR.putpixel((x,y), 255)
                else:
                    maskR.putpixel((x,y), 0)
                count += 1
    
    #display the mask
    qim = ImageQt(maskR)
    pixMap = QtGui.QPixmap.fromImage(qim)
    self.maskDisplay.setPixmap(pixMap)
    maskR.save("maskR.png")

    print("Encoding Green Channel...")
    while count <= img.size[0] * img.size[1] * 2 and count < len(codestr):
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                self.progressBar.setProperty("value", ( count / len(codestr) ) * 100)
                if codestr[count:count+1] == "1":
                    maskG.putpixel((x,y), 255)
                else:
                    maskG.putpixel((x,y), 0)
                count += 1
    #display the mask
    if count < len(codestr):
        qim = ImageQt(maskG)
        pixMap = QtGui.QPixmap.fromImage(qim)
        self.maskDisplay.setPixmap(pixMap)
        maskR.save("maskG.png")

    print("Encoding Blue Channel...")
    while count <= img.size[0] * img.size[1] * 3 and count < len(codestr):
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                self.progressBar.setProperty("value", ( count / len(codestr) ) * 100)
                if codestr[count:count+1] == "1":
                    maskB.putpixel((x,y), 255)
                else:
                    maskB.putpixel((x,y), 0)
                count += 1
    #display the mask
    if count < len(codestr):
        qim = ImageQt(maskB)
        pixMap = QtGui.QPixmap.fromImage(qim)
        self.maskDisplay.setPixmap(pixMap)
        maskR.save("maskB.png")

    self.label_2.setText("Compiling Image...")
    self.progressBar.setProperty("value", 0)

    print("Making Encoded Image...")
    # Change the channels
    r, g, b, a = img.split()
    nr, ng, nb = r, g, b
    self.progressBar.setProperty("value", 10)

    r = r.point(makeEven)
    nr = r.point(makeOdd)
    r.paste(nr, None, maskR)
    self.progressBar.setProperty("value", 45)

    g = g.point(makeEven)
    ng = g.point(makeOdd)
    g.paste(ng, None, maskG)
    self.progressBar.setProperty("value", 70)

    b = b.point(makeEven)
    nb = b.point(makeOdd)
    b.paste(nb, None, maskB)
    self.progressBar.setProperty("value", 95)


    # Save it
    img = Image.merge("RGB", (r, g, b))

    encodeend = time.time()
    encodetime = encodeend - encodestart
    print("Image Encoded in " + str(round(encodetime,2)) + " seconds.")
    self.progressBar.setProperty("value", 100)
    self.label_2.setText("Complete")


   
    return img

def decode(self, imagePath):
    decodestart = time.time()
    print("Reading Raw Binary...")
    img = Image.open(imagePath)
    r,g,b = img.split()
    r = r.point(oddWhiteEvenBlack)
    g = g.point(oddWhiteEvenBlack)
    b = b.point(oddWhiteEvenBlack)
    rawBinary = ""
    print("Reading Red Channel Binary...")
    for x in range(r.size[0]):
        for y in range(r.size[1]):
            if r.getpixel((x,y)) % 2 == 1:
                rawBinary += "1"
            else:
                rawBinary += "0"
    print("Reading Green Channel Binary...")
    for x in range(g.size[0]):
        for y in range(g.size[1]):
            if g.getpixel((x,y)) % 2 == 1:
                rawBinary += "1"
            else:
                rawBinary += "0"
    print("Reading Blue Channel Binary...")
    for x in range(b.size[0]):
        for y in range(b.size[1]):
            if b.getpixel((x,y)) % 2 == 1:
                rawBinary += "1"
            else:
                rawBinary += "0"
    print("Splitting Raw Binary into Bytes...")
    count = 0
    rawBinaryList = list()
    for num in range(int(len(rawBinary)/8)):
        rawBinaryList.append(int(rawBinary[count:count+8],2))
        count += 8

    print("Process Completed.")

    return rawBinaryList