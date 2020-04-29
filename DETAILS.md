# System Requirements

## 🟡 Import an image into the program (BMP, PNG, JPG) 

❌ ~~Check the hex file signature to ensure the file is indeed an image~~ 

✔ Program shall ensure that a valid image has been provided for input 

## ✔ Import files into the program 

✔ Ensure that the file isn’t too big to encode in the selected image 

✔ Ensure that an image has been selected beforehand 

✔ Program shall provide useful and context specific error messages 

## ✔ Allow the user to choose between encoding and decoding files 

✔ Select options using a drop down menu 

✔ Encode and decode with every encoding method 

## ✔ Display the encoding/decoding process 

✔ Visual display for appropriate methods 

✔ Progress bar 

## 🟡 Allow the user to choose between encoding steganography methods 

✔ LSB (RGB Pixel Encoding) 

❌ ~~PVD (Pixel Value Differencing)~~ 

❌ ~~Noise Manipulation~~ 

✔ Appending after the trailer hex (concatenation)

## ✔ Export the encoded image 

✔ Export the file to user-selected file name and directory 

# Test Plan

## Show the proper encoding and decoding of data
- A file will be encoded into an image file and decoded using both LSB and Concatenation methods.
- Through this test, most other test requirements should be met.

## Import images/files into the program
- This requirement will be met several times while testing the other requirements of the program.

## Allow the user to choose between encoding/decoding and steganography methods
- Display the combobox dropdown menus at the top of the program

## Display the encoding/decoding process 
- The middle window during the LSB encoding process should display a static-like image during the progress of encoding, showing which pixels are being altered.
- The progress bar should update with the progress of encoding/decoding during all methods.

## Export the encoded image 
- The encoded images will be exported in order to import them back into the program and show the decoding method.
