from PyQt5.QtCore import QDir, Qt, QUrl, QTimer, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QCheckBox)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont
import sys
from prawo_test import pytanie, media, nr_pytan, odpowiedz_a, odpowiedz_b, odpowiedz_c, poprawna_odpowiedz, wylosowano

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Prawo Jazdy") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()
        videoWidget.setMinimumHeight(600)

        self.numer_pytania = 0

        self.odpowiedzi_uzytkownika = {
            0 : "", 1 : "", 2 : "", 3 : "", 4 : "", 5 : "", 6 : "", 7 : "", 8 : "", 9 : "", 10 : "", 11 : "", 12 : "", 13 : "", 14 : "", 15 : "", 
            16 : "", 17 : "", 18 : "", 19 : "", 20 : "", 21 : "", 22 : "", 23 : "", 24 : "", 25 : "", 26 : "", 27 : "", 28 : "", 29 : "", 30 : "", 31 : ""
        }

        self.poprawne_odpowiedzi = {
            0 : "", 1 : "", 2 : "", 3 : "", 4 : "", 5 : "", 6 : "", 7 : "", 8 : "", 9 : "", 10 : "", 11 : "", 12 : "", 13 : "", 14 : "", 15 : "", 
            16 : "", 17 : "", 18 : "", 19 : "", 20 : "", 21 : "", 22 : "", 23 : "", 24 : "", 25 : "", 26 : "", 27 : "", 28 : "", 29 : "", 30 : "", 31 : ""
        }

        for i in range(32):
            self.poprawne_odpowiedzi[i] = str(poprawna_odpowiedz[nr_pytan[i]]).strip("(),'")

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.showAnsButton = QPushButton()
        self.showAnsButton.setText("Sprawdź odpowiedź")
        self.showAnsButton.setFixedWidth(360)
        self.showAnsButton.clicked.connect(self.show_ans)

        self.changeModeButton = QPushButton()
        self.changeModeButton.setText("Tryb testu")
        self.changeModeButton.setCheckable(True)

        self.answerButton1 = QCheckBox()
        self.answerButton2 = QCheckBox()
        self.answerButton3 = QCheckBox()
        self.answerButton1.setFixedWidth(32)
        self.answerButton2.setFixedWidth(32)
        self.answerButton3.setFixedWidth(32)
        self.answerButton1.setFixedHeight(30)
        self.answerButton2.setFixedHeight(30)
        self.answerButton3.setFixedHeight(30)
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

        self.nr_pytaniaLabel = QLabel()
        self.nr_pytaniaLabel.setAlignment(Qt.AlignCenter)
        self.nr_pytaniaLabel.setFixedHeight(30)
        self.ilosc_wylosowania_pytaniaLabel = QLabel()
        self.ilosc_wylosowania_pytaniaLabel.setAlignment(Qt.AlignCenter)
        self.ilosc_wylosowania_pytaniaLabel.setFixedHeight(30)

        self.questionLabel = QLabel(wordWrap=True)
        self.questionLabel.setMinimumHeight(50)
        self.questionLabel.setMaximumHeight(1000)

        self.answerLabel1 = QLabel(wordWrap=True)
        self.answerLabel1.setMinimumHeight(30)
        self.answerLabel1.setMaximumHeight(150)

        self.answerLabel2 = QLabel(wordWrap=True)
        self.answerLabel2.setMinimumHeight(30)
        self.answerLabel2.setMaximumHeight(150)

        self.answerLabel3 = QLabel(wordWrap=True)
        self.answerLabel3.setMinimumHeight(30)
        self.answerLabel3.setMaximumHeight(150)

        self.answerButton1.setStyleSheet("""QCheckBox::indicator {width: 32px; height: 32px;
                                         }
                                         QCheckBox::indicator:unchecked {image: url(Box.png);
                                         }
                                         QCheckBox::indicator:checked {image: url(TickBox.png);
                                         }""")
        self.answerButton2.setStyleSheet("""QCheckBox::indicator {width: 32px; height: 32px;
                                         }
                                         QCheckBox::indicator:unchecked {image: url(Box.png);
                                         }
                                         QCheckBox::indicator:checked {image: url(TickBox.png);
                                         }""")
        self.answerButton3.setStyleSheet("""QCheckBox::indicator {width: 32px; height: 32px;
                                         }
                                         QCheckBox::indicator:unchecked {image: url(Box.png);
                                         }
                                         QCheckBox::indicator:checked {image: url(TickBox.png);
                                         }""")

        font = QFont()
        font2 = QFont()
        font.setPointSize(24)
        font2.setPointSize(18)
        self.showAnsButton.setFont(font)
        self.previous_question.setFont(font)
        self.next_question.setFont(font)
        self.endButton.setFont(font)
        self.changeModeButton.setFont(font)
        self.questionLabel.setFont(font2)
        self.nr_pytaniaLabel.setFont(font2)
        self.ilosc_wylosowania_pytaniaLabel.setFont(font2)
        self.answerLabel1.setFont(font2)
        self.answerLabel2.setFont(font2)
        self.answerLabel3.setFont(font2)

        self.ilosc_pytan = QLabel()
        self.ilosc_pytan.setAlignment(Qt.AlignCenter)
        self.ilosc_pytan.setFont(font2)

        self.globalnyCzas = QLabel()
        self.globalnyCzas.setAlignment(Qt.AlignCenter)
        self.globalnyCzas.setFont(font2)
        self.globalnyCzas.setHidden(True)
        self.globalnyCzas.setFixedHeight(30)

        self.pytanieCzas = QLabel()
        self.pytanieCzas.setAlignment(Qt.AlignCenter)
        self.pytanieCzas.setFont(font2)
        self.pytanieCzas.setFixedHeight(30)
        self.pytanieCzas.setHidden(True)

        self.errorLabel = QLabel()
        self.errorLabel.setHidden(True)
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

        questionLayout = QHBoxLayout()
        questionLayout.setContentsMargins(0, 0, 0, 0)
        questionLayout.addWidget(self.previous_question)
        questionLayout.addWidget(self.ilosc_pytan)
        questionLayout.addWidget(self.next_question)

        okLayout = QHBoxLayout()
        okLayout.setContentsMargins(0, 0, 0, 0)
        okLayout.addWidget(self.questionLabel)
        okLayout.addWidget(self.showAnsButton)
        okLayout.addWidget(self.pytanieCzas)

        answerLayout1 = QHBoxLayout()
        answerLayout1.setContentsMargins(0, 0, 0, 0)
        answerLayout1.addWidget(self.answerButton1)
        answerLayout1.addWidget(self.answerLabel1)

        answerLayout2 = QHBoxLayout()
        answerLayout2.setContentsMargins(0, 0, 0, 0)
        answerLayout2.addWidget(self.answerButton2)
        answerLayout2.addWidget(self.answerLabel2)

        answerLayout3 = QHBoxLayout()
        answerLayout3.setContentsMargins(0, 0, 0, 0)
        answerLayout3.addWidget(self.answerButton3)
        answerLayout3.addWidget(self.answerLabel3)

        endLayout = QHBoxLayout()
        endLayout.addWidget(self.changeModeButton)
        endLayout.addWidget(self.endButton)

        layout = QVBoxLayout()
        layout.addLayout(endLayout)
        layout.addSpacing(50)
        layout.addWidget(self.globalnyCzas)
        layout.addWidget(self.nr_pytaniaLabel)
        layout.addWidget(self.ilosc_wylosowania_pytaniaLabel)
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        layout.addLayout(okLayout)
        layout.addLayout(answerLayout1)
        layout.addLayout(answerLayout2)
        layout.addLayout(answerLayout3)
        layout.addSpacing(50)
        layout.addLayout(questionLayout)
        

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.answerLabel1.mousePressEvent = self.label_click1
        self.answerLabel2.mousePressEvent = self.label_click2
        self.answerLabel3.mousePressEvent = self.label_click3
        videoWidget.mousePressEvent = self.video_click

        self.changeModeButton.pressed.connect(self.testMode)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def label_click1(self, *arg, **kwargs):
        if self.answerButton1.isChecked():
            self.answerButton1.setChecked(False)
        else:
            self.answerButton1.setChecked(True)
            
            self.answerButton2.setChecked(False)
            self.answerButton3.setChecked(False)
    def label_click2(self, *arg, **kwargs):
        if self.answerButton2.isChecked():
            self.answerButton2.setChecked(False)
        else:
            self.answerButton2.setChecked(True)

            self.answerButton1.setChecked(False)
            self.answerButton3.setChecked(False)
    def label_click3(self, *arg, **kwargs):
        if self.answerButton3.isChecked():
            self.answerButton3.setChecked(False)
        else:
            self.answerButton3.setChecked(True)

            self.answerButton1.setChecked(False)
            self.answerButton2.setChecked(False)

    def video_click(self, *arg, **kwargs):
        self.play()

    def openFile(self):
        if str(media[nr_pytan[self.numer_pytania]]).strip("(),") != '':
            video = str(media[nr_pytan[self.numer_pytania]]).strip("(),'")
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(f'wizualizacje/{video}')))
            self.playButton.setEnabled(True)
            if("jpg" in video):
                self.playButton.click()

    def exitCall(self):
        sys.exit(app.exec_())

    def testMode(self):
        if(not self.changeModeButton.isChecked()):
            self.showAnsButton.setHidden(True)
            self.previous_question.setHidden(True)
            self.pytanieCzas.setHidden(False)
            self.globalnyCzas.setHidden(False)
            self.timer = QTimer()
            self.timerGlobal = QTimer()
            self.timerQuestion = QTimer()

            self.timeGlobal = QTime(00,25,00)
            self.timeQuestion = QTime(00,00,35)

            self.timer.start(1000)
            self.timer.timeout.connect(self.addSec)

            self.timerQuestion.start(35_000)
            self.timerGlobal.start(1_500_000)

            self.globalnyCzas.setText(self.timeGlobal.toString("mm:ss"))
            self.pytanieCzas.setText(self.timeQuestion.toString("mm:ss"))

            self.timerGlobal.timeout.connect(lambda: self.endButton.click())
            self.timerQuestion.timeout.connect(lambda: self.next_question.click())
        else:
            self.timer.stop()
            self.timerGlobal.stop()
            self.timerQuestion.stop()

            self.showAnsButton.setHidden(False)
            self.previous_question.setHidden(False)
            self.pytanieCzas.setHidden(True)
            self.globalnyCzas.setHidden(True)

    def addSec(self):
        self.timeGlobal = self.timeGlobal.addSecs(-1)
        self.timeQuestion = self.timeQuestion.addSecs(-1)
        self.globalnyCzas.setText(self.timeGlobal.toString("mm:ss"))
        self.pytanieCzas.setText(self.timeQuestion.toString("mm:ss"))

    def previous(self):
        if(self.odpowiedz_b == ''):
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
        if(self.odpowiedz_b == ''):
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

        if(self.changeModeButton.isChecked()):
            self.timerQuestion.start(35_000)
            self.timer.start(1000)
            self.timeQuestion = QTime(00,00,35)
            self.globalnyCzas.setText(self.timeGlobal.toString("mm:ss"))
            self.pytanieCzas.setText(self.timeQuestion.toString("mm:ss"))
                
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

    def show_ans(self):
        self.answerButton1.setChecked(False)
        self.answerButton2.setChecked(False)
        self.answerButton3.setChecked(False)
        if(self.poprawne_odpowiedzi[self.numer_pytania] == "A" or self.poprawne_odpowiedzi[self.numer_pytania] == "Tak"):
            self.answerButton1.setChecked(True)
            self.answerLabel1.setStyleSheet(
                "background-color : lightgreen"
            )
        elif(self.poprawne_odpowiedzi[self.numer_pytania] == "B"):
            self.answerButton2.setChecked(True)
            self.answerLabel2.setStyleSheet(
                "background-color : lightgreen"
            )
        elif(self.poprawne_odpowiedzi[self.numer_pytania] == "C" or self.poprawne_odpowiedzi[self.numer_pytania] == "Nie"):
            self.answerButton3.setChecked(True)
            self.answerLabel3.setStyleSheet(
                "background-color : lightgreen"
            )

    def refresh(self):
        self.nr_pytaniaLabel.setText(f"Pytanie {self.numer_pytania+1}")
        self.ilosc_wylosowania_pytaniaLabel.setText(f"Pytanie zostało wylosowane {str(wylosowano[nr_pytan[self.numer_pytania]]).strip("(),'")} raz{"y" if str(wylosowano[nr_pytan[self.numer_pytania]]).strip("(),'") != "1" else ""}")

        #odmiany
        self.ilosc_pytan.setText(f"Pozostał{"o" if not ((4 >=(31-self.numer_pytania) % 10 >= 2) and not(14 >= 31-self.numer_pytania >= 12)) else "y"} {31-self.numer_pytania} {'pytań' if( (((31-self.numer_pytania) % 10) >= 5 or 1>=(31-self.numer_pytania)%10>=0 or (20>=31-self.numer_pytania >= 10)) and (31-self.numer_pytania != 1)) else "pytania" if(31-self.numer_pytania != 1) else "pytanie"}")
        
        self.question = str(pytanie[nr_pytan[self.numer_pytania]]).strip("(),'")
        self.odpowiedz_a = str(odpowiedz_a[nr_pytan[self.numer_pytania]]).strip("(),'")
        self.odpowiedz_b = str(odpowiedz_b[nr_pytan[self.numer_pytania]]).strip("(),'")
        self.odpowiedz_c = str(odpowiedz_c[nr_pytan[self.numer_pytania]]).strip("(),'")

        if(self.odpowiedz_b == ''):
            self.answerLabel1.setText("Tak.")
            self.answerLabel3.setText("Nie.")
            self.answerButton2.setHidden(True)
            self.answerLabel2.setHidden(True)
        else:
            self.answerLabel1.setText("A: " + self.odpowiedz_a)
            self.answerLabel2.setText("B: " + self.odpowiedz_b)
            self.answerLabel3.setText("C: " + self.odpowiedz_c)
            self.answerButton2.setHidden(False)
            self.answerLabel2.setHidden(False)

        self.questionLabel.setText(self.question)
        
        if(self.numer_pytania == 0):
            self.previous_question.setEnabled(False)
        elif(self.numer_pytania == 31):
            self.next_question.setEnabled(False)
        else:
            self.next_question.setEnabled(True)
            self.previous_question.setEnabled(True)

        self.answerButton1.setChecked(False)
        self.answerButton2.setChecked(False)
        self.answerButton3.setChecked(False)

        self.answerButton1.adjustSize()
        self.answerButton2.adjustSize()
        self.answerButton3.adjustSize()

        self.answerLabel1.setStyleSheet(
                "background-color : #f0f0f0"
            )
        self.answerLabel2.setStyleSheet(
                "background-color : #f0f0f0"
            )
        self.answerLabel3.setStyleSheet(
                "background-color : #f0f0f0"
            )

        if(self.odpowiedzi_uzytkownika[self.numer_pytania] != ''):
            if(self.odpowiedzi_uzytkownika[self.numer_pytania] == "A" or self.odpowiedzi_uzytkownika[self.numer_pytania] == "Tak"):
                self.answerButton1.setChecked(True)
            elif(self.odpowiedzi_uzytkownika[self.numer_pytania] == "B"):
                self.answerButton2.setChecked(True)
            elif(self.odpowiedzi_uzytkownika[self.numer_pytania] == "C" or self.odpowiedzi_uzytkownika[self.numer_pytania] == "Nie"):
                self.answerButton3.setChecked(True)

        # print(self.odpowiedzi_uzytkownika)

        self.errorLabel.setText('')
        self.errorLabel.setHidden(True)

        self.openFile()

    def show_marks(self):
        if(self.changeModeButton.isChecked()):
            self.timer.stop()
            self.timerGlobal.stop()
            self.timerQuestion.stop()
            
        if(self.odpowiedz_b == ''):
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

        punkty = 0
        text = ""
        text_błędne = ""
        for i in range(32):
            text += str(i+1) + "." + " Twoja odpowiedź: "+ str(self.odpowiedzi_uzytkownika[i]) + "\n" + "Poprawna odpowiedź: " + str(self.poprawne_odpowiedzi[i]) + "\n\n"
            if(str(poprawna_odpowiedz[nr_pytan[i]]).strip("(),'") == self.odpowiedzi_uzytkownika[i]):
                punkty += 1
            else:
                text_błędne += str(i+1) + "." + " Twoja odpowiedź: "+ str(self.odpowiedzi_uzytkownika[i]) + "\n" + "Poprawna odpowiedź: " + str(self.poprawne_odpowiedzi[i]) + "\n\n"

        wyniki = QMessageBox()
        wyniki.setWindowTitle("Wyniki")
        wyniki.setText(f'{punkty}/32, czyli {float(punkty/32)*100}%')

        wyniki.addButton("OK", QMessageBox.ButtonRole.AcceptRole)

        custom_button = QPushButton("Pokaż błędne")
        custom_button.setCheckable(True)

        font = QFont()
        font.setPointSize(24)
        wyniki.setFont(font)
        wyniki.setDetailedText(text)

        wyniki.addButton(custom_button, QMessageBox.ButtonRole.NoRole)
        custom_button.disconnect()

        def sprawdz_bledne():
            if(not custom_button.isChecked()):
                wyniki.setDetailedText(text_błędne)
            else:
                wyniki.setDetailedText(text)

        custom_button.pressed.connect(sprawdz_bledne)

        for widget in wyniki.findChildren(QTextEdit):
            widget.setFont(QFont("Arial", 24))  # Set font size
            widget.setFixedSize(400, 600)

        wyniki.exec_()
        if(self.changeModeButton.isChecked()):
            exit(0)

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
        self.errorLabel.setHidden(False)
        self.errorLabel.setText("Brak mediów do tego pytania.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(1920,1080)
    player.show()
    player.refresh()
    sys.exit(app.exec_())