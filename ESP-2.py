from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageFilter, ImageDraw
from PIL.ImageQt import ImageQt
import re
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
    '''
    # 13 = PE_PanelButtonCommand
    # 03 = PE_FrameFocusRect
    # 19 = PE_IndicatorArrowDown
    def drawPrimitive(self, element, option, painter, w = 0):
        #print(element)
        super().drawPrimitive(element, option, painter, w)

    # 0  = CE_PushButton
    # 1  = CE_PushButtonBevel
    # 2  = CE_PushButtonLabel
    # 20 = CE_MenuBarItem
    # 21 = CE_MenuBarEmptyArea
    # 39 = CE_ComboBoxLabel
    # 46 = CE_ShapedFrame
    def drawControl(self, element, option, painter, w = 0):
        print(element)
        super().drawControl(element, option, painter, w)

    def drawComplexControl(self, element, option, painter, w = 0):
        print(element)
        super().drawComplexControl(element, option, painter, w)
    '''

class App(QWidget):

    stegoImage = Image.new('RGB', (20,20), 'black')
    originImagePath = ""
    outputFilePath = ""
    documentPath = ""
    bi1 = Image.new('RGB', (300,300), 'white')
    basicImage = QImage(300, 300, QImage.Format_RGB32)
    tInImage = QImage(300, 300, QImage.Format_RGB32)
    tOutImage = QImage(300, 300, QImage.Format_RGB32)
    fileOutput = ""
    type = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def saveFileDialog(self):
        self.fileOutput = "maskG.png"
        if self.fileOutput:
            fType = filetype.guess(self.fileOutput)
            if fType == None:
                formatText = "Text File (*.txt)\n"
            else:
                name = re.match(r"[^/]*", fType.mime)
                ext = re.search(r"(?<=/).*", fType.mime)
                name = ext.group(0).upper() + " " + name.group(0)[:1].upper() + name.group(0)[1:]
                formatText = name + " (*." + fType.extension + ")\n"
            formatText += "All Files (*.*)"
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Output File","",formatText)
            if fileName:
                fileout = open(fileName, "wb+")
                for i in self.fileOutput:
                    fileout.write(bytes([i]))
                fileout.close()

    def saveImageDialog(self):
        if self.stegoImage:
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Output Image","","BMP Image (*.bmp)\nPNG Image (*.png)")
            if fileName:
                self.stegoImage.save(fileName)

    def chooseFileDialog(self, label):
        if (self.originImagePath == ""):
            popup = QMessageBox.critical(self, "Error", "Please select an image to encode before choosing a file", QMessageBox.Ok)
        else:
            fileName, _ = QFileDialog.getOpenFileName(self,"Choose a File", "","Text Files (*.*)")
            if fileName:
                if (os.stat(self.originImagePath).st_size / 8) <= (os.stat(fileName).st_size):
                    popup = QMessageBox.critical(self, "Error", "Your selected file is too big to encrypt in your selected image. Select a different file or image.", QMessageBox.Ok)
                else:
                    self.documentPath = fileName
                    label.setText("File: "+self.documentPath)

    def chooseImageDialog(self, label):
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose Input Image", "","BMP Files (*.bmp)")
        if fileName:
            self.originImagePath = fileName
        try:
            pixMap = QPixmap(fileName)
            label.setPixmap(pixMap)
        except:
            print("error")

    def initUI(self):
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # IMPORT IMAGE BUTTON
        self.importButton = QPushButton("Import Image...")
        self.importButton.clicked.connect(lambda: self.chooseImageDialog(self.inputImageGraphic))
        self.mainLayout.addWidget(self.importButton, 0, 0, 1, 2)

        # File to ENCODE
        self.fileButton = QPushButton("Import File...")
        self.fileButton.clicked.connect(lambda: self.chooseFileDialog(self.fileLabel))
        self.mainLayout.addWidget(self.fileButton, 1, 0, 1, 2)

        # ENCODE / DECODE
        self.cryptBox = QComboBox()
        self.cryptBox.addItem("Encode")
        self.cryptBox.addItem("Decode")
        self.mainLayout.addWidget(self.cryptBox, 0, 2)

        # ALGORITHM TYPE
        self.methodBox = QComboBox()
        self.methodBox.addItem("LSB")
        self.mainLayout.addWidget(self.methodBox, 0, 3)

        # START BUTTON
        self.startButton = QPushButton("Run")
        #self.startButton.clicked.connect(lambda: self.run_stego_function())
        self.mainLayout.addWidget(self.startButton, 1, 2, 1, 2)

        # SAVE STEGO IMAGE
        self.saveButton = QPushButton("Save Image...")
        self.saveButton.clicked.connect(lambda: self.saveImageDialog())
        self.mainLayout.addWidget(self.saveButton, 0, 4, 1, 2)

        # SAVE STEGO FILE
        self.saveFileButton = QPushButton("Save File...")
        self.saveFileButton.clicked.connect(lambda: self.saveFileDialog())
        self.mainLayout.addWidget(self.saveFileButton, 1, 4, 1, 2)

        # Input image display
        self.inputImageGraphic = QLabel()
        self.mainLayout.addWidget(self.inputImageGraphic, 2, 0, 2, 2, Qt.AlignCenter)

        iPixMap = QPixmap.fromImage(self.tInImage)
        self.inputImageGraphic.setPixmap(iPixMap)

        # mask display
        self.maskDisplay = QLabel()
        self.mainLayout.addWidget(self.maskDisplay, 2, 2, 2, 2, Qt.AlignCenter)

        pixMap = QPixmap.fromImage(self.basicImage)
        self.maskDisplay.setPixmap(pixMap)

        # Export image display
        self.outputImageGraphic = QLabel()
        # SOMETHING HERE
        self.outputImageGraphic.setMargin(150)
        self.outputImageGraphic.setIndent(100)
        self.mainLayout.addWidget(self.outputImageGraphic, 2, 4, 2, 2, Qt.AlignCenter)

        oPixMap = QPixmap.fromImage(self.tOutImage)
        self.outputImageGraphic.setPixmap(oPixMap)

        # LABELS
        self.inputLabel = QLabel("Input Image")
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.inputLabel, 4, 0, 1, 2)

        self.processLabel = QLabel("Image Processing")
        self.processLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.processLabel,4,2,1,2)

        self.outputLabel = QLabel("Output Image")
        self.outputLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.outputLabel, 4, 4, 1, 2)

        self.fileLabel = QLabel("File:")
        self.fileLabel.setAlignment(Qt.AlignLeft)
        #self.mainLayout.addWidget(self.fileLabel, 1,2,1,2)

        self.progressBar = QProgressBar()
        self.progressBar.setProperty("value", 0 )

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

        actionImport_Image = QAction("&Import Image", self)
        actionImport_Image.setShortcut("Ctrl+I")
        actionImport_Image.triggered.connect(lambda: self.mainWidget.chooseFileDialog(self.mainWidget.inputImageGraphic))

        actionImport_File = QAction("&Import File", self)
        actionImport_File.setShortcut("Ctrl+Alt+I")
        actionImport_File.triggered.connect(lambda: self.mainWidget.chooseFileDialog(self.mainWidget.fileLabel))

        actionExport_Image = QAction("&Export Image", self)
        actionExport_Image.setShortcut("Ctrl+E")
        actionExport_Image.triggered.connect(lambda: self.mainWidget.saveImageDialog())

        actionExport_File = QAction("&Export File", self)
        actionExport_File.setShortcut("Ctrl+Alt+E")
        actionExport_File.triggered.connect(lambda: self.mainWidget.saveFileDialog())

        actionExit_Program = QAction("&Exit Program", self)
        actionExit_Program.triggered.connect(lambda: self.close())

        actionCancel_Current_Process = QAction("&Cancel Process", self)
        actionCancel_Current_Process.setShortcut("Ctrl+C")
        #actionCancel_Current_Process.triggered.connect()

        menuFile.addAction(actionExit_Program)
        menuFile.addAction(actionCancel_Current_Process)

        menuFile.addAction(actionImport_Image)
        menuFile.addAction(actionExport_Image)
        menuFile.addAction(actionImport_File)
        menuFile.addAction(actionExport_File)


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
