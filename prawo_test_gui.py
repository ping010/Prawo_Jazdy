from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QCheckBox)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QIcon
import sys
import random
import mysql.connector
from prawo_test import pytanie, media, nr_pytan, odpowiedz_a, odpowiedz_b, odpowiedz_c, poprawna_odpowiedz

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.numer_pytania = 0

        self.odpowiedzi_uzytkownika = {
            0 : "", 1 : "", 2 : "", 3 : "", 4 : "", 5 : "", 6 : "", 7 : "", 8 : "", 9 : "", 10 : "", 11 : "", 12 : "", 13 : "", 14 : "", 15 : "", 16 : "", 17 : "", 18 : "", 19 : "",
            20 : "", 21 : "", 22 : "", 23 : "", 24 : "", 25 : "", 26 : "", 27 : "", 28 : "", 29 : "", 30 : "", 31 : "", 32 : "", 33 : "", 34 : "", 35 : "", 36 : "", 37 : "", 38 : "", 39 : ""
        }

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.answerButton1 = QCheckBox()
        self.answerButton2 = QCheckBox()
        self.answerButton3 = QCheckBox()
        self.answerButton1.clicked.connect(self.uncheck1)
        self.answerButton2.clicked.connect(self.uncheck2)
        self.answerButton3.clicked.connect(self.uncheck3)

        self.next_question = QPushButton()
        self.previous_question = QPushButton()
        self.next_question.setText("Następne pytanie")
        self.previous_question.setText("Poprzednie pytanie")
        self.next_question.clicked.connect(self.next)
        self.previous_question.clicked.connect(self.previous)
        self.previous_question.setEnabled(False)

        self.endButton = QPushButton()
        self.endButton.setText("Zakończ test")
        self.endButton.clicked.connect(self.show_marks)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.questionLabel = QLabel()

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        answerLayout = QHBoxLayout()
        answerLayout.setContentsMargins(0, 0, 0, 0)
        answerLayout.addWidget(self.previous_question)
        answerLayout.addWidget(self.answerButton1)
        answerLayout.addWidget(self.answerButton2)
        answerLayout.addWidget(self.answerButton3)
        answerLayout.addWidget(self.next_question)

        endLayout = QHBoxLayout()
        endLayout.addWidget(self.endButton)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.questionLabel)
        layout.addLayout(answerLayout)
        layout.addSpacing(50)
        layout.addLayout(endLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.refresh()

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        if str(media[nr_pytan[self.numer_pytania]]).strip("(),") != '':
            video = str(media[nr_pytan[self.numer_pytania]]).strip("(),'")
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(f'wizualizacje/{video}')))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def previous(self):
        if(self.odpowiedz_a == ''):
            if(self.answerButton1.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "Tak"
            elif(self.answerButton3.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "Nie"
        else:
            if(self.answerButton1.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "A"
            elif(self.answerButton2.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "B"
            elif(self.answerButton3.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "C"

        self.numer_pytania -= 1
        self.refresh()

    def next(self):
        if(self.odpowiedz_a == ''):
            if(self.answerButton1.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "Tak"
            elif(self.answerButton3.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "Nie"
        else:
            if(self.answerButton1.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "A"
            elif(self.answerButton2.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "B"
            elif(self.answerButton3.isChecked()):
                self.odpowiedzi_uzytkownika[self.numer_pytania] = "C"
                
        self.numer_pytania += 1
        self.refresh()

    def uncheck1(self):
        self.answerButton2.setChecked(False)
        self.answerButton3.setChecked(False)

    def uncheck2(self):
        self.answerButton1.setChecked(False)
        self.answerButton3.setChecked(False)

    def uncheck3(self):
        self.answerButton1.setChecked(False)
        self.answerButton2.setChecked(False)

    def refresh(self):
        self.question = str(pytanie[nr_pytan[self.numer_pytania]]).strip("(),'")
        self.odpowiedz_a = str(odpowiedz_a[nr_pytan[self.numer_pytania]]).strip("(),'")
        self.odpowiedz_b = str(odpowiedz_b[nr_pytan[self.numer_pytania]]).strip("(),'")
        self.odpowiedz_c = str(odpowiedz_c[nr_pytan[self.numer_pytania]]).strip("(),'")

        if(self.odpowiedz_a == ''):
            self.answerButton1.setText("Tak.")
            self.answerButton3.setText("Nie.")
            self.answerButton2.setHidden(True)
        else:
            self.answerButton1.setText("A: " + self.odpowiedz_a)
            self.answerButton2.setText("B: " + self.odpowiedz_b)
            self.answerButton3.setText("C: " + self.odpowiedz_c)
            self.answerButton2.setHidden(False)

        self.questionLabel.setText(self.question)
        
        if(self.numer_pytania == 0):
            self.previous_question.setEnabled(False)
        elif(self.numer_pytania == 39):
            self.next_question.setEnabled(False)
        else:
            self.next_question.setEnabled(True)
            self.previous_question.setEnabled(True)

        self.answerButton1.setChecked(False)
        self.answerButton2.setChecked(False)
        self.answerButton3.setChecked(False)

        if(self.odpowiedzi_uzytkownika[self.numer_pytania] != ''):
            if(self.odpowiedzi_uzytkownika[self.numer_pytania] == "A" or self.odpowiedzi_uzytkownika[self.numer_pytania] == "Tak"):
                self.answerButton1.setChecked(True)
            elif(self.odpowiedzi_uzytkownika[self.numer_pytania] == "B"):
                self.answerButton2.setChecked(True)
            elif(self.odpowiedzi_uzytkownika[self.numer_pytania] == "C" or self.odpowiedzi_uzytkownika[self.numer_pytania] == "Nie"):
                self.answerButton3.setChecked(True)

        print(self.odpowiedzi_uzytkownika)

        self.errorLabel.setText('')

        self.openFile()

    def show_marks(self):
        punkty = 0
        for i in range(40):
            if(str(poprawna_odpowiedz[nr_pytan[i]]).strip("(),'") == self.odpowiedzi_uzytkownika[i]):
                punkty += 1

        wyniki = QMessageBox()
        wyniki.setWindowTitle("Wyniki")
        wyniki.setText(f'{punkty}/40, czyli {float(punkty/40)*100}%')
        wyniki.exec_()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Brak mediów do tego pytania.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())