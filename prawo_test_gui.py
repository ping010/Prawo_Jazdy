from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys
import random
import mysql.connector
# from prawo_test import media, nr_pytan

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

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

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="Ezmysql@1",
          database="producto"
        )

        #Adding a mysql cursor
        cursor = db.cursor()

        #Importing data from mysql into lists
        pytanie = []
        media = []
        odpowiedz_a, odpowiedz_b, odpowiedz_c = [],[],[]
        poprawna_odpowiedz = []
        cursor.execute("SELECT Pytanie FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
        for question in cursor:
                pytanie.append(question)

        cursor.execute("SELECT Media FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
        for m in cursor:
                media.append(m)

        cursor.execute("SELECT `Odpowiedź A` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
        for a in cursor:
                odpowiedz_a.append(a)

        cursor.execute("SELECT `Odpowiedź B` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
        for b in cursor:
                odpowiedz_b.append(b)

        cursor.execute("SELECT `Odpowiedź C` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
        for c in cursor:
                odpowiedz_c.append(c)

        cursor.execute("SELECT `Poprawna odp` FROM pytania_egzminacyjne WHERE Kategorie LIKE '%B%' ")
        for po in cursor:
                poprawna_odpowiedz.append(po)

        #Selecting 40 random questions
        print(str(media[0]).strip("(),"))
        is_changed = False
        nr_pytan = []
        for _ in range(40):
                i = random.randint(0,2014)
                while(not is_changed):
                            if(i not in nr_pytan):
                                    is_changed = True
                            else:
                                    i = random.randint(0,2014)
                is_changed = False
                nr_pytan.append(i)
        print(str(media[nr_pytan[0]]).strip("(),'"))
        if str(media[nr_pytan[0]]).strip("(),") != '':
            meida = str(media[nr_pytan[0]]).strip("(),'")
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(f'wizualizacje/{meida}')))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

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
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())