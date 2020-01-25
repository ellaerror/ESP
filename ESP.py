from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageFilter, ImageDraw
from PIL.ImageQt import ImageQt
import os
import sys
import RGBCE
import filetype

class DarkWinStyle(QProxyStyle):
    def __init__(self):
        super().__init__(QStyleFactory.create('Windows'))

    def standardPalette(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.Base, QColor(75, 75, 75))
        dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ButtonText, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.Highlight, QColor(152, 202, 235))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        dark_palette.setColor(QPalette.Background, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.Light, QColor(150, 150, 150))
        dark_palette.setColor(QPalette.Midlight, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.Dark, QColor(5, 5, 5))
        dark_palette.setColor(QPalette.Shadow, QColor(0, 0, 0))

        return dark_palette

class App(QWidget):

    stegoImage = Image.new('RGB', (20,20), 'black')
    originImagePath = ""
    outputFilePath = ""
    documentPath = ""
    bi1 = Image.new('RGB', (300,300), 'white')
    basicImage = QImage(300, 300, QImage.Format_RGB32)
    fileOutput = ""
    type = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # IMPORT IMAGE BUTTON
        self.importButton = QPushButton("Import Image...")
        #self.importButton.clicked.connect(self.import_image)
        self.mainLayout.addWidget(self.importButton)

        # File to ENCODE
        self.fileButton = QPushButton("Import File...")
        #self.fileButton.clicked.connect(lambda: self.import_file())
        self.mainLayout.addWidget(self.fileButton)

        # ENCODE / DECODE
        self.cryptBox = QComboBox()
        self.cryptBox.addItem("Encode")
        self.cryptBox.addItem("Decode")
        self.mainLayout.addWidget(self.cryptBox)

        # ALGORITHM TYPE
        self.methodBox = QComboBox()
        self.methodBox.addItem("rgbce")
        self.mainLayout.addWidget(self.methodBox)

        '''
        # START BUTTON
        self.startButton = QToolButton(self.horizontalLayoutWidget)
        self.startButton.setStyleSheet("border: 4px, solid, rgb(255,255,255)")
        self.horizontalLayout.addWidget(self.startButton)
        self.startButton.clicked.connect(lambda: self.run_stego_function())

        # SAVE STEGO IMAGE
        self.saveButton = QToolButton(self.horizontalLayoutWidget)
        self.saveButton.setStyleSheet("border: 4px, solid, rgb(255,255,255)")
        self.horizontalLayout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(lambda: self.save_image())

        # more horizontal layout stuff
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 30, 771, 171))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        # Input image display
        self.inputImageGraphic = QLabel(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.addWidget(self.inputImageGraphic)

        # mask display
        self.maskDisplay = QLabel(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.addWidget(self.maskDisplay)

        pixMap = QPixmap.fromImage(self.basicImage)
        imageHeight = int(((MainWindow.width()/3) * pixMap.height()) / pixMap.width())
        pixMap = pixMap.scaled(int(MainWindow.width()/3), imageHeight )
        self.maskDisplay.setPixmap(pixMap)
        self.maskDisplay.resize(int(MainWindow.width()/3),int(MainWindow.width()/3))

        # Export image display
        self.outputImageGraphic = QLabel(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.addWidget(self.outputImageGraphic)

        # LABELS
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 201, 251, 16))
        self.label.setAlignment(Qt.AlignCenter)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(260, 230, 251, 16))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QRect(520, 230, 251, 16))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setGeometry(QRect(0, 230, 251, 16))
        self.label_4.setAlignment(Qt.AlignCenter)

        # Encoding Progress Bar

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(260, 200, 251, 23))
        self.progressBar.setProperty("value", 0 )

        MainWindow.setCentralWidget(self.centralwidget)
        '''

class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup main window
        self.setWindowTitle("ESP")
        self.mainWidget = App(parent=self)
        self.setCentralWidget(self.mainWidget)
        qApp.setStyle(DarkWinStyle())
        qApp.setPalette(self.style().standardPalette())

        # Menu Bar Main
        menuBar = self.menuBar()
        menuFile = menuBar.addMenu('&File')
        menuEdit = menuBar.addMenu('&Edit')

        actionImport_Image = QAction("&Import Image", self)
        actionImport_Image.setShortcut("Ctrl+I")
        #actionImport_Image.triggered.connect(lambda: )

        actionExport_Image = QAction("&Export Image", self)
        actionExport_Image.setShortcut("Ctrl+E")
        #actionExport_Image.triggers.connect(lambda: )

        actionExit_Program = QAction("&Exit Program", self)
        actionExit_Program.triggered.connect(lambda: self.close())

        actionCancel_Current_Process = QAction("&Cancel Process", self)
        actionCancel_Current_Process.setShortcut("Ctrl+C")
        #actionCancel_Current_Process.triggered.connect()

        menuFile.addAction(actionExit_Program)
        menuFile.addAction(actionCancel_Current_Process)

        menuEdit.addAction(actionImport_Image)
        menuEdit.addAction(actionExport_Image)

    def import_file(self):
        try:
            # If no image is selected, throw an error
            if self.originImagePath == "" :
                popup = QtWidgets.QMessageBox.critical(self, "No image file selected", "Please select an image to encode before choosing a file", QMessageBox.Ok)
            else:
                getFile = QFileDialog()
                getFile.setFileMode(QFileDialog.AnyFile)
                if getFile.exec_():
                    documentPath = getFile.selectedFiles()
                # if the file isn't 1/8 or less the size of the image it's too big!
                if (os.stat(self.originImagePath).st_size / 8) <= (os.stat(documentPath[0]).st_size):
                    popup = QtWidgets.QMessageBox.critical(self, "File too big", "Your selected file is too big to encrypt in your selected image. Select a different file or image.", QMessageBox.Ok)
                else:
                    # save the verified file path
                    self.documentPath = documentPath[0]
                    _translate = QtCore.QCoreApplication.translate
                    self.label_4.setText(_translate("MainWindow", "File: "+self.documentPath))
        except:
            print("No File Selected or Unsupported File Type")

    def import_image(self):
        getFile = QFileDialog()
        getFile.setFileMode(QFileDialog.AnyFile)
        if getFile.exec_():
            imageName = getFile.selectedFiles()
        try:
            sinImgName = imageName[0]
            self.originImagePath = sinImgName

            # Change image so it fits nicely
            pixMap = QPixmap(sinImgName)
            imageHeight = int(((MainWindow.width()/3) * pixMap.height()) / pixMap.width())
            pixMap = pixMap.scaled(int(MainWindow.width()/3), imageHeight )

            # Resize layout
            MainWindow.resize(MainWindow.width(), MainWindow.height() + imageHeight-(int(MainWindow.width()/3))+75)
            self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 30, 771, 171 + (imageHeight-171)))
            self.label.setGeometry(QtCore.QRect(0, (200 + imageHeight)-171, 251, 16))
            self.label_2.setGeometry(QtCore.QRect(260, (230 + imageHeight)-171, 251, 16))
            self.label_3.setGeometry(QtCore.QRect(520, (230 + imageHeight)-171, 251, 16))
            self.label_4.setGeometry(QtCore.QRect(0, (230 + imageHeight)-171, 251, 16))
            self.progressBar.setGeometry(QtCore.QRect(260, (200 + imageHeight)-171, 251, 23))

            # Set image
            self.inputImageGraphic.setPixmap(pixMap)
            self.inputImageGraphic.resize(int(MainWindow.width()/3),int(MainWindow.width()/3))
        except:
            print("No File Selected or Unsupported File Type")

#LOOK HEREEEE
    def save_image(self):
        if (str(self.cryptBox.currentText()) == "Encode"):
            # get file path to save in
            filePath = QFileDialog.getSaveFileName(MainWindow, '', 'stego-output', 'BMP (*.bmp)\nPNG (*.png)')

            # save the image
            self.stegoImage.save(filePath[0])
        else:
            if self.type == None:
                formatText = "txt (*.txt)"
            else:
                formatText = str(self.type.extension) + " (*." + str(self.type.extension) + ")"
            filePath = QFileDialog.getSaveFileName(MainWindow, '', 'stego-output', formatText)
            fileout = open(filePath[0], "wb+")
            for i in self.fileOutput:
                fileout.write(bytes([i]))
            fileout.close()

    def run_stego_function(self):

        if (str(self.methodBox.currentText()) == "RGBCE (RGB Channel Encoding)"):

            if (str(self.cryptBox.currentText()) == "Encode" ):
                self.stegoImage = RGBCE.encode(self, self.originImagePath, self.documentPath)

                # display the image
                qim = ImageQt(self.stegoImage)
                pixMap = QtGui.QPixmap.fromImage(qim)
                imageHeight = int(((MainWindow.width()/3) * pixMap.height()) / pixMap.width())
                pixMap = pixMap.scaled(int(MainWindow.width()/3), imageHeight )
                self.outputImageGraphic.setPixmap(pixMap)
                self.outputImageGraphic.resize(int(MainWindow.width()/3),int(MainWindow.width()/3))

            if (str(self.cryptBox.currentText()) == "Decode" ):
                self.fileOutput = RGBCE.decode(self, self.originImagePath)

                #Save temp file
                fileout = open("temp", "wb+")
                for i in self.fileOutput:
                    fileout.write(bytes([i]))

                # determine file type
                self.type = filetype.guess("temp")
                if self.type is None:
                    self.outputImageGraphic.setText("Decoded file type is .txt or unknown")
                else:
                    self.outputImageGraphic.setText("Decoded file type is " + self.type.extension)

                # delete temp file
                fileout.close()
                os.remove("temp")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ESP - Ella's Steganography Program"))
        self.importButton.setText(_translate("MainWindow", "Import Image..."))
        self.cryptBox.setItemText(0, _translate("MainWindow", "Encode"))
        self.cryptBox.setItemText(1, _translate("MainWindow", "Decode"))
        self.methodBox.setItemText(0, _translate("MainWindow", "RGBCE (RGB Channel Encoding)"))
        self.fileButton.setText(_translate("MainWindow", "Import File..."))
        self.saveButton.setText(_translate("MainWindow", "Save Stego Object..."))
        self.startButton.setText(_translate("MainWindow", "Start Process..."))
        self.label.setText(_translate("MainWindow", "Input Image"))
        self.label_2.setText(_translate("MainWindow", "Image Processing"))
        self.label_3.setText(_translate("MainWindow", "Output Image"))
        self.label_4.setText(_translate("MainWindow", "No File Selected"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImport_Image.setText(_translate("MainWindow", "Import Image"))
        self.actionExport_Image.setText(_translate("MainWindow", "Export Image"))
        self.actionExit_Program.setText(_translate("MainWindow", "Exit Program"))
        self.actionCancel_Current_Process.setText(_translate("MainWindow", "Cancel Current Process"))

if __name__ == "__main__":
    app = QApplication([])
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
