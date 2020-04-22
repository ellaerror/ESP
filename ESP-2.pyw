from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageFilter, ImageDraw
from PIL.ImageQt import ImageQt
import re
import os
import sys
import LSB
import Concatenate
import filetype
import xml.etree.ElementTree as ET

class PrefObject():

    def __init__(self, id, name=None, value=None, description = None):
        try:
            self.id = int(id)
        except:
            raise Exception('Expected type of \'int\' for value \'id\'')
        self.name = name
        self.value = value
        self.description = description

    def __str__(self):
        string = "{'id': '"+str(self.id)+"',"

        string += " 'name': "
        if self.name:
            string += "'"+str(self.name)+"', "
        else:
            string += "'', "

        string += " 'value': "
        if self.value:
            string += "'"+str(self.value)+"', "
        else:
            string += "'', "

        string += " 'description': "
        if self.description:
            string += "'"+str(self.description)+"'"
        else:
            string += "''"

        string += "}"
        return string

    def __repr__(self):
        string = "{'id': '"+str(self.id)+"',"

        string += " 'name': "
        if self.name:
            string += "'"+str(self.name)+"', "
        else:
            string += "'', "

        string += " 'value': "
        if self.value:
            string += "'"+str(self.value)+"', "
        else:
            string += "'', "

        string += " 'description': "
        if self.description:
            string += "'"+str(self.description)+"'"
        else:
            string += "''"

        string += "}"
        return string

class LightWinStyle(QProxyStyle):

    def __init__(self):
        super().__init__(QStyleFactory.create('Windows'))

    def drawControl(self, element, opt, p, widget = None):
        if element == 11 or element == 13:
            pass
        elif element == 12:
            opt.palette.setColor(QPalette.Highlight, QColor(129, 184, 48))
            opt.rect = QRect(2, 1, widget.size().width()-2, widget.sizeHint().height()-2)
            super().drawControl(element, opt, p, widget)
        else:
            super().drawControl(element, opt, p, widget)

    def pixelMetric(self, pm, opt = None, w = None):
        if pm == 24:
            if w:
                return w.size().width() / 100
            else:
                return 1
        else:
            return super().pixelMetric(pm, opt, w)

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

    def drawControl(self, element, opt, p, widget = None):
        if element == 11 or element == 13:
            pass
        elif element == 12:
            opt.palette.setColor(QPalette.Highlight, QColor(86, 133, 17))
            opt.rect = QRect(2, 1, widget.size().width()-2, widget.sizeHint().height()-2)
            super().drawControl(element, opt, p, widget)
        else:
            super().drawControl(element, opt, p, widget)

    def pixelMetric(self, pm, opt = None, w = None):
        if pm == 24:
            if w:
                return w.size().width() / 100
            else:
                return 1
        else:
            return super().pixelMetric(pm, opt, w)

class ELabel(QLabel):
    Image = None
    File = ""
    penWidth = 1
    penColor = QColor(0,0,0)

    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.setMinimumSize(20, 20)

    def paintEvent(self, event):
        if self.Image:
            p = QPixmap(self.Image)

            w = self.width()
            h = self.height()

            self.setPixmap(p.scaled(w,h,1))
        super().paintEvent(event)

    def resizeEvent(self, event):
        if self.Image:
            p = QPixmap(self.Image)

            w = self.width()
            h = self.height()

            self.setPixmap(p.scaled(w,h,1))
        super().resizeEvent(event)

    def setImage(self, image):
        if image.width() > 400:
            w = 400
        else:
            w = image.width()
        if image.height() > 400:
            h = 400
        else:
            h = image.height()
        self.setMinimumSize(w,h)
        self.Image = image
        p = QPixmap(image)
        np = p.scaled(w,h,2)
        self.setPixmap(np)

    def setFile(self, file):
        self.File = file
        self.Image = QImage(file)

class App(QWidget):

    stegoImage = Image.new('RGB', (20,20), 'black')
    originImagePath = ""
    outputFilePath = ""
    documentPath = ""
    bi1 = Image.new('RGB', (400,400), 'white')
    basicImage = QImage(400, 400, QImage.Format_ARGB32)
    tInImage = QImage(400, 400, QImage.Format_ARGB32)
    tOutImage = QImage(400, 400, QImage.Format_ARGB32)
    fileOutput = ""
    type = ""
    imageQLabels = []
    inputFileData = []
    imageBytes = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def saveFileDialog(self):
        if self.fileOutput:
            fType = self.type
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
                if type(self.fileOutput[0]) == type(b'7'):
                    for i in self.fileOutput:
                        fileout.write(i)
                else:
                    for i in self.fileOutput:
                        fileout.write(bytes([i]))
                fileout.close()
            self.saveFileButton.setStyleSheet("")

    def saveImageDialog(self):
        if self.imageBytes:
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Output Image","","BMP Image (*.bmp)\nPNG Image (*.png)\nAll Files (*.*)")
            if fileName:
                output = open(fileName, 'wb')
                count = 0
                for byte in self.imageBytes:
                    try:
                        output.write(byte)
                    except:
                        print("ERROR",count,byte)
                    count+=1
                output.close()
            self.imageBytes = None
        elif self.stegoImage:
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Output Image","","BMP Image (*.bmp)\nPNG Image (*.png)\nAll Files (*.*)")
            if fileName:
                self.stegoImage.save(fileName)

    def chooseFileDialog(self, label):
        if (self.originImagePath == ""):
            popup = QMessageBox.critical(self, "Error", "Please select an image to encode before choosing a file", QMessageBox.Ok)
        else:
            fileName, _ = QFileDialog.getOpenFileName(self,"Choose a File", "","Text Files (*.*)")
            if fileName:
                if (os.stat(self.originImagePath).st_size / 8) <= (os.stat(fileName).st_size) and self.methodBox.currentText()== "LSB":
                    popup = QMessageBox.critical(self, "Error", "Your selected file is too big to encrypt in your selected image. Select a different file or image.", QMessageBox.Ok)
                else:
                    try:
                        self.documentPath = fileName
                        self.inputFileData = []
                        input = open(fileName, 'rb')
                        byte = input.read(1)
                        while byte:
                            self.inputFileData.append(bytes(byte))
                            byte = input.read(1)
                        label.setText("File: "+self.documentPath)
                        input.close()
                    except Exception as exp:
                        popup = QMessageBox.critical(self, "Error", "Unexpected Error: " + str(exp), QMessageBox.Ok)

    def chooseImageDialog(self, label):
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose Input Image", "","Image Files (*.bmp;*.png;*.jpg)")
        if fileName:
            self.originImagePath = fileName
            try:
                pixMap = QPixmap(fileName)
                label.setPixmap(pixMap.scaled(label.pixmap().width(), label.pixmap().height(), Qt.KeepAspectRatio))
                label.setImage(QImage(fileName))

                clearImg = QImage(label.pixmap().width(), label.pixmap().height(), QImage.Format_ARGB32)

                self.maskDisplay.setImage(clearImg)
                self.outputImageGraphic.setImage(clearImg)

                self.maskDisplay.setPixmap(QPixmap.fromImage(clearImg))
                self.outputImageGraphic.setPixmap(QPixmap.fromImage(clearImg))

                label.setFile(fileName)
            except Exception as exp:
                print(exp)

    def runStegoFunction(self):
        if (str(self.cryptBox.currentText()) == "Encode" ):
            if not self.stegoImage:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Please choose an image.")
                msg.exec()
                return
            elif len(self.inputFileData) <= 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Please choose a file.")
                msg.exec()
                return
            elif self.methodBox.currentText() == "LSB":
                self.stegoImage = LSB.encode(self, self.originImagePath, self.inputFileData)
            elif self.methodBox.currentText() == "Concatenate":
                self.imageBytes = Concatenate.encode(self, self.originImagePath, self.inputFileData)
                self.stegoImage = QImage(self.originImagePath)

            # display the image
            #qim = ImageQt(self.stegoImage)
            pixMap = QPixmap.fromImage(self.stegoImage)
            pixMap = pixMap.scaled(self.outputImageGraphic.pixmap().width(), self.outputImageGraphic.pixmap().height())
            self.outputImageGraphic.setImage(self.stegoImage)
            self.outputImageGraphic.setPixmap(pixMap)

        if (str(self.cryptBox.currentText()) == "Decode" ):
            if self.methodBox.currentText() == "LSB":
                self.fileOutput = LSB.decode(self, self.originImagePath)
            elif self.methodBox.currentText() == "Concatenate":
                self.fileOutput = Concatenate.decode(self, self.originImagePath)
            else:
                return

            #Save temp file
            fileout = open("temp", "wb+")
            if type(self.fileOutput[0]) == type(b'7'):
                for i in self.fileOutput:
                    fileout.write(i)
            else:
                for i in self.fileOutput:
                    fileout.write(bytes([i]))

            # determine file type
            self.type = filetype.guess("temp")
            message = "File type is unknown"
            if self.type is None:
                message = "Decoded file type is .txt or unknown"
            else:
                message = "Decoded file type is " + self.type.extension

            self.saveFileButton.setStyleSheet("background-color: #f5d442")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Decoded")
            msg.setText(message)
            msg.exec()

            # delete temp file
            fileout.close()
            os.remove("temp")

    def paintEvent(self, event):
        painter = QPainter(self)

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
        self.methodBox.addItem("Concatenate")
        self.mainLayout.addWidget(self.methodBox, 0, 3)

        # START BUTTON
        self.startButton = QPushButton("Run")
        self.startButton.clicked.connect(lambda: self.runStegoFunction())
        self.mainLayout.addWidget(self.startButton, 1, 2, 1, 2)

        # SAVE STEGO IMAGE
        self.saveButton = QPushButton("Save Image...")
        self.saveButton.clicked.connect(lambda: self.saveImageDialog())
        self.mainLayout.addWidget(self.saveButton, 0, 4, 1, 2)

        # SAVE STEGO FILE
        self.saveFileButton = QPushButton("Save File...")
        self.saveFileButton.clicked.connect(lambda: self.saveFileDialog())
        self.mainLayout.addWidget(self.saveFileButton, 1, 4, 1, 2)

        barPalette = self.style().standardPalette()
        #highlight is bar color
        barPalette.setColor(QPalette.Window, qApp.palette().color(QPalette.Background))

        self.progressBar = QProgressBar()
        self.progressBar.setPalette(barPalette)
        #self.progressBar.setStyleSheet("border: 0px; padding: 1px;")
        self.progressBar.setMaximumHeight(28)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        #self.progressBar.setTextVisible(False)

        self.progressFrame = QFrame()
        self.progressFrame.setMaximumHeight(28)
        self.progressFrame.setFrameShape(QFrame.StyledPanel)
        self.progressFrame.setFrameShadow(QFrame.Sunken)

        barLayout = QHBoxLayout()
        barLayout.addWidget(self.progressBar)
        self.progressFrame.setLayout(barLayout)

        barLayout.setSpacing(0)
        barLayout.setContentsMargins(0,0,0,0)

        self.mainLayout.addWidget(self.progressFrame, 5, 0, 1, 6)

        # Input image display
        self.inputImageGraphic = ELabel()
        self.inputImageGraphic.setFrameShape(QFrame.StyledPanel)
        self.inputImageGraphic.setFrameShadow(QFrame.Sunken)
        #self.inputImageGraphic.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.mainLayout.addWidget(self.inputImageGraphic, 2, 0, 2, 2, Qt.AlignTop and Qt.AlignCenter)
        iPixMap = QPixmap.fromImage(self.tInImage)
        self.inputImageGraphic.setImage(self.tInImage)
        self.inputImageGraphic.setPixmap(iPixMap)
        self.imageQLabels.append(self.inputImageGraphic)

        # mask display
        self.maskDisplay = ELabel()
        self.maskDisplay.setFrameShape(QFrame.StyledPanel)
        self.maskDisplay.setFrameShadow(QFrame.Sunken)
        #self.maskDisplay.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.mainLayout.addWidget(self.maskDisplay, 2, 2, 2, 2, Qt.AlignTop and Qt.AlignCenter)
        pixMap = QPixmap.fromImage(self.basicImage)
        self.maskDisplay.setImage(self.basicImage)
        self.maskDisplay.setPixmap(pixMap)
        self.imageQLabels.append(self.maskDisplay)

        # Export image display
        self.outputImageGraphic = ELabel()
        self.outputImageGraphic.setFrameShape(QFrame.StyledPanel)
        self.outputImageGraphic.setFrameShadow(QFrame.Sunken)
        #self.outputImageGraphic.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.mainLayout.addWidget(self.outputImageGraphic, 2, 4, 2, 2, Qt.AlignTop and Qt.AlignCenter)
        oPixMap = QPixmap.fromImage(self.tOutImage)
        self.outputImageGraphic.setImage(self.tOutImage)
        self.outputImageGraphic.setPixmap(oPixMap)
        self.imageQLabels.append(self.outputImageGraphic)

        # LABELS
        self.inputLabel = QLabel("Input Image")
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.inputLabel, 4, 0, 1, 2, Qt.AlignTop)

        self.processLabel = QLabel("Image Processing")
        self.processLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.processLabel,4,2,1,2, Qt.AlignTop)

        self.outputLabel = QLabel("Output Image")
        self.outputLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.outputLabel, 4, 4, 1, 2, Qt.AlignTop)

        self.fileLabel = QLabel("File:")
        self.fileLabel.setAlignment(Qt.AlignLeft)
        #self.mainLayout.addWidget(self.fileLabel, 1,2,1,2)

class Window(QMainWindow):

    mainWidget = None
    prefFile = "lib\\pref.xml"
    prefTree = None
    prefRoot = None
    prefList = []

    # TODO
    def preferenceUI(self):
        pass

    def editPreferences(self):
        self.preferenceUI()
        root = ET.Element("pref")
        tree = ET.ElementTree(root)
        for pref in self.prefList:
            root.append(ET.Element("option", {"id":str(pref.id)}))
            root[pref.id].append(ET.Element("name"))
            root[pref.id][0].text = str(pref.name)
            root[pref.id].append(ET.Element("value"))
            root[pref.id][1].text = str(pref.value)
            root[pref.id].append(ET.Element("description"))
            root[pref.id][2].text = str(pref.description)
        tree.write(self.prefFile)
        self.loadPreferences()

    def loadPreferences(self):
        if not self.prefExists():
            self.initPreferences()
            return
        self.prefTree = ET.parse(self.prefFile)
        self.prefRoot = self.prefTree.getroot()
        for child in self.prefRoot:
            pref = PrefObject(child.attrib['id'])
            for grandchild in child:
                setattr(pref, grandchild.tag, grandchild.text)
            self.prefList.append(pref)
        if len(self.prefList) <= 0:
            self.initPreferences()

    def initPreferences(self):
        pref = open(self.prefFile, 'w+')
        self.prefList = [PrefObject(0, "Dark Mode", False, "Use dark mode on start-up")]
        root = ET.Element("pref")
        tree = ET.ElementTree(root)
        for pref in self.prefList:
            root.append(ET.Element("option", {"id":str(pref.id)}))
            root[pref.id].append(ET.Element("name"))
            root[pref.id][0].text = str(pref.name)
            root[pref.id].append(ET.Element("value"))
            root[pref.id][1].text = str(pref.value)
            root[pref.id].append(ET.Element("description"))
            root[pref.id][2].text = str(pref.description)
        tree.write(self.prefFile)
        self.loadPreferences()

    def prefExists(self):
        try:
            pref = open(self.prefFile, 'r')
            pref.close()
            return True
        except:
            return False

    def darkMode(self):
        qApp.setStyle(DarkWinStyle())
        qApp.setPalette(self.style().standardPalette())

    def lightMode(self):
        qApp.setStyle(LightWinStyle())
        qApp.setPalette(self.style().standardPalette())

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadPreferences()

        if self.prefList[0].value == "True":
            qApp.setStyle(DarkWinStyle())
        else:
            qApp.setStyle(LightWinStyle())

        # Setup main window
        self.setWindowTitle("ESP")
        qApp.setPalette(self.style().standardPalette())
        #print(qApp.palette().color(QPalette.Background).getRgb())
        self.mainWidget = App(parent=self)
        self.setCentralWidget(self.mainWidget)

        # Menu Bar Main
        menuBar = self.menuBar()
        menuFile = menuBar.addMenu('&File')
        menuEdit = menuBar.addMenu('&Edit')

        actionImport_Image = QAction("&Import Image", self)
        actionImport_Image.setShortcut("Ctrl+I")
        actionImport_Image.triggered.connect(lambda: self.mainWidget.chooseImageDialog(self.mainWidget.inputImageGraphic))

        actionImport_File = QAction("&Import File", self)
        actionImport_File.setShortcut("Ctrl+Alt+I")
        actionImport_File.triggered.connect(lambda: self.mainWidget.chooseFileDialog(self.mainWidget.fileLabel))

        actionExport_Image = QAction("&Export Image", self)
        actionExport_Image.setShortcut("Ctrl+E")
        actionExport_Image.triggered.connect(lambda: self.mainWidget.saveImageDialog())

        actionEdit_Preferences = QAction("&Edit Preferences", self)
        actionEdit_Preferences.triggered.connect(lambda: self.editPreferences())

        actionExport_File = QAction("&Export File", self)
        actionExport_File.setShortcut("Ctrl+Alt+E")
        actionExport_File.triggered.connect(lambda: self.mainWidget.saveFileDialog())

        actionExit_Program = QAction("&Exit Program", self)
        actionExit_Program.triggered.connect(lambda: self.close())

        actionEnable_Dark_Mode = QAction("&Enable Dark Mode", self)
        actionEnable_Dark_Mode.triggered.connect(lambda: self.darkMode())

        actionEnable_Light_Mode = QAction("&Enable Light Mode", self)
        actionEnable_Light_Mode.triggered.connect(lambda: self.lightMode())

        menuFile.addAction(actionExit_Program)

        menuFile.addAction(actionImport_Image)
        menuFile.addAction(actionExport_Image)
        menuFile.addAction(actionImport_File)
        menuFile.addAction(actionExport_File)

        menuEdit.addAction(actionEdit_Preferences)
        menuEdit.addAction(actionEnable_Dark_Mode)
        menuEdit.addAction(actionEnable_Light_Mode)

if __name__ == "__main__":
    app = QApplication([])
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
