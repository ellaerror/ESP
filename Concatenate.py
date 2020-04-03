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
import os

def encode(self, imagePath, fileBytes):
    self.progressBar.setProperty("value", 0)
    espTrailer = [b'45',b'53',b'50',b'161',b'30']
    trailer = True
    imageBytes = []
    if "png" in imagePath:
        trailer = True
    elif "jpg" in imagePath:
        trailer = True
    else:
        trailer = False

    input = open(imagePath, 'rb')
    byte = input.read(1)
    while byte:
        imageBytes.append(bytes(byte))
        byte = input.read(1)
    input.close()

    if not trailer:
        for byte in espTrailer:
            imageBytes.append(bytes)

    for byte in fileBytes:
        imageBytes.append(byte)

    self.progressBar.setProperty("value", 100)
    return imageBytes

def decode(self, imagePath):
    if "png" in imagePath:
        trailer = [b'I',b'E',b'N',b'D',b'\xAE', b'B', b'`', b'\x82', b',']
    elif "jpg" in imagePath:
        trailer = [b'\xff',b'\xd9']
    else:
        trailer = [b'45',b'53',b'50',b'161',b'30']
    self.progressBar.setProperty("value", 0)

    imageBytes =[]
    input = open(imagePath, 'rb')
    byte = input.read(1)
    while byte:
        imageBytes.append(bytes(byte))
        byte = input.read(1)
    input.close()

    index = 0
    count = 0
    found = False
    trailerEnd = -1
    for byte in imageBytes:
        if byte == trailer[index] and not found and count >= 15:
            index+=1
            if index == len(trailer):
                found = True
                trailerEnd = count
                break
        else:
            index = 0
        count+=1
    self.progressBar.setProperty("value", 100)
    return imageBytes[count+1:]
