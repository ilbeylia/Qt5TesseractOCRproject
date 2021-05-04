from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2 as cv
import pytesseract as pytr
import os
from gtts import gTTS

pytr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(623, 478)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(601, 351))
        self.label.setMaximumSize(QtCore.QSize(601, 351))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Giris.png"))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.CamStart)
        self.pushButton_2.clicked.connect(self.LoadImage)
        self.pushButton.clicked.connect(self.label.clear)
        # self.pushButton_2.clicked.connect(self.textEdit.clear)
        self.pushButton_3.clicked.connect(self.to_speech)
        self.pushButton_4.clicked.connect(self.to_pdf)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # add code
        self.filename = None  # will hold the image  address
        self.tmp = None       # will hold the temporary image for display
        self.tmp_frame= None  # will hold the temporary frame for display
        self.started= False   # Cam Button status

# image OCR
    def LoadImage(self):  # user selected image
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv.imread(self.filename)
        self.setPhoto(self.image)
        self.pytr(self.image)


    def setPhoto(self, image):
        self.tmp = image
        frame = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def pytr(self,image):     #pytesseract --> OCR
        text = pytr.image_to_string(image,lang='tur')  #language options lang='eng'
        self.textEdit.setText(text)
        self.textEdit.setReadOnly(True)

    def to_speech(self):  # text to speech
        text = self.textEdit.toPlainText()
        read = gTTS(text, lang='tr')   #language options lang='eng'
        read.save('to_speech.wav')
        os.system('to_speech.wav')


    def to_pdf(self):   # to pdf write and save
        img = self.tmp
        to_pdf= pytr.image_to_pdf_or_hocr(img)
        with open('to_pdf.pdf', 'wb') as pdf:
            pdf.write(to_pdf)


#Cam OCR

    def CamStart(self):
        if self.started:
            self.started= False
            self.pushButton.setText('Start Cam')

        else:
            self.started=True
            self.pushButton.setText('Stop Cam')

        cam= True
        if cam:
            cap=cv.VideoCapture(0)
        else:
            cap= cv.VideoCapture('OCR.mp4')   # will come ...
        while True:
            ret, self.frame = cap.read()

            #pytesseract --> OCR     *** increase reading speed
            frame= self.frame
            hImg, wImg, _ = frame.shape

            # conf = r'--oem 3 --psm 6'
            boxes = pytr.image_to_data(frame,lang='tur')   #language options lang='eng'
            for a, b in enumerate(boxes.splitlines()):
                # print(b)
                if a != 0:
                    b = b.split()
                    if len(b) == 12:
                        x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        cv.putText(frame, b[11], (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 1) # in the update section
                        cv.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
                        text=b[11]
                        # print(text)
                        self.textEdit.append(text)
                        self.textEdit.setReadOnly(True)

            self.setFrame(self.frame)

            # self.update()

            key = cv.waitKey(1) & 0xFF
            if self.started == False:
                break

    def setFrame(self, frame):
        self.tmp_frame = frame
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(frame))

    # def update(self,frame):  # Here we add display text to the image







    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OCR"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">OCR(<span style=\" font-family:\'sans-serif\'; font-size:14px; font-weight:600; color:#202122; background-color:#ffffff;\">Optical Character Recognition</span>)</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Start Cam"))
        self.pushButton_2.setText(_translate("MainWindow", "Load Image"))
        self.pushButton_3.setText(_translate("MainWindow", "To Speech"))
        self.pushButton_4.setText(_translate("MainWindow", "To Pdf"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
