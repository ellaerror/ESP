# ESP - Ella's Steganography Program

## Prerequsites

- [Python 3](https://www.python.org/downloads/)
- PyQt5 `pip install PyQt5`
- Pillow `pip install Pillow`

This program runs and has been tested on Windows 10 with Python 3.8.

## Installation

After installing the prerequsities, download this repository as a zip and unzip it or simply clone it to your home computer. 

For ease of access in running the program, ensure that [Python 3 is added to your Path variable](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path).

## Running the Program

To run the program, double-click the ESP-2.pyw file. If you have set up your computer to open python files with a text editor by default, you may have to right-click the file and click open with > python. This should run the program. If you have troubles running the program in this manner, you can run the program by running the command `pyw ESP-2.pyw` in the console.

The usage of **pyw** versus the normal **py** simply removes the background console from appearing. 

## Using the Program

### Importing an Image

To import a file to encode or decode, either press the "Import Image" button, press "Ctrl+I", or click "File">"Import Image". 

![Importing an Image 1](https://imgur.com/MawYeuA.png)
![Importing an Image 2](https://imgur.com/Hu9Cp2a.png)

### Importing a File

When importing a file to encode into an image, you may press the "Import File" button, press "Ctrl+Alt+I", or click "File">"Import File". 

When using the LSB encoding method, files must be an eighth of the size of the image to be encoded. This is due to the method of encoding, there's simply not enough space in the image for all the data in the file. 

![Importing a File 1](https://imgur.com/TMGMpPp.png)
![Importing a File 2](https://imgur.com/tJdnxNp.png)

### Exporting Your Encoded Image

When exporting your encoded image, be mindful of the file format you export it as.

When using the LSB encoding method, export using a *lossless* file format such as a PNG or BMP file. Files such as JPGs will not properly store the data and it will be lost. 

When using the Concatenation encoding method, ensure that you're saving the image as the SAME file format as you imported it as. For example, if you encoded a JPG image, save the encoded image as a JPG. Compression does not matter with this method of encoding. 

Encoded images can be exported by pressing the "Save Image" button, pressing "Ctrl+E", or clicking "File">"Export Image"

![Exporting an Image 1](https://imgur.com/pczG2xs.png)
![Exporting an Image 2](https://imgur.com/l1LvE91.png)

### Exporting Decoded Files

After decoding a hidden file, you can export it by pressing the "Save File" button, pressing "Ctrl+Alt+E", or clicking "File">"Export File"

If the program is able to successfully detect what kind of file was encoded, it should tell you when the save dialog opens up. Otherwise, you can choose the option to save it as any file extension if you're aware of the original file type. The file type is determined based on the header bytes of the file using the python filetype module. 

![Exporting a File 1](https://imgur.com/NkWa8DI.png)
![Exporting a File 2](https://imgur.com/5KO8qJY.png)

# Encoding Method Details

## LSB - Least Significant Bit

**Important**: Because of the way LSB encodes data, image compression will completely destory any data encoded in the image. Saving LSB encoded images in JPG images or any other compressed image form will corrupt and destroy the encoded data.

### Encoding Method

To encode the data into an image, ESP utilizes the Pillow module in python to alter the pixel values of the image. 

First, the program splits the image into three channels, red, blue, and green. It also takes the file data and converts it from bytes to a binary string. 

For every binary bit in the file data, it either changes a pixel value in the image to even or odd. It traverses columns first, then rows, and it goes through the red channel first, then green, then blue. It attempts to display this process in the center portion of the program by displaying which pixels are changed as they're altered. 

The channels are recombined after they are encoded and sent back to the main program to be saved.

### Decoding Method

To decode the data in an LSB encoded image, the program splits apart the channels again in order to read the data. In the same way that it encoded the data, the program goes back and checks whether each pixel color is even or odd. Depending on the value, it adds the appropriate binary bit to a string containing the total data of the decoded file.

The binary string is then transformed back into bytes and sent back to the main program to be saved.

## Concatenation

**Important**: Currently the only supported image formats to reliably decode are **PNG** and **JPG**. You may attempt to encode any other image types but decoding may not be reliable due to the lack of trailer bytes. 

### Encoding Method

Concatenation is a pretty simple encoding method. The imported image and file are transferred into the program as bytes and appended together. From there, they are written to the file name chosen from the user. 

### Decoding Method

To decode a concatenated file, the program first takes in the imported image as bytes. It determines the file type based off of the file extension of the file, and looks for the trailer bytes of the image file. Once it determines where the image file ends, it returns remaining bytes to the main program. There, it attempts to determine the file type and the file is available to be saved. 
