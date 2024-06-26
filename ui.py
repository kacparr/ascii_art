import random
import sys
import string
import random
from pathlib import Path
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *


class _WindowBar(QWidget):
    def __init__(self) :
        super().__init__()
        self.setFixedSize(800,30)
        layout = QHBoxLayout()
        self.icon = QLabel()
        self.title = QLabel("Ascii art!")
        self.title.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title)
        self.setLayout(layout)


    def paintEvent(self,e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('#000181'))
        brush.setStyle(QtCore.Qt.SolidPattern)
        bar = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())            
        painter.fillRect(bar, brush)
        
    def sizeHint(self):
        return QtCore.QSize(1,1)

class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ASCII Generator")
        self.setFixedSize(800,630)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.FramelessWindowHint)
        
        
        self.hello = ["Siemaneczko", "eluwina"]
        with open("palette.hex","r") as f:
            self.palette = [x.strip() for x in f.readlines()]
        self.letter_table = [x for x in string.printable]
        self.letters = [self.create_letter(random.choice(self.letter_table)) for _ in range(150)]
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(25)
        
        
        layout = QVBoxLayout()
        self._windowbar = _WindowBar()
        layout.addWidget(self._windowbar)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.button = QPushButton("ELO!")
        self.button2 = QPushButton("Press button 2 to xd.")
        self.text = QLabel("elo")   
        self.text2 = QLabel("")

        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.text)
        layout.addWidget(self.text2)
        self.button.clicked.connect(self.magic)
        self.button2.clicked.connect(self.xd)

    def create_letter(self, char):
        letter = QLabel(char, self)
        letter.setStyleSheet(f'font-size: {random.randint(8,32)}px; color: #{random.choice(self.palette)}')
        x = random.randint(0, self.width())         
        y = random.randint(30, self.height())
        letter.move(x, y)
        letter.show()
        return letter
    
    def animation(self):
        for letter in self.letters:
            x = letter.x() + 2
            if x > self.width()+1:
                letter.setText(random.choice(self.letter_table))
                x = 0
                y = random.randint(30, self.height())
                letter.move(x,y)
            else:
                letter.move(x,letter.y())
            

    
    def magic(self):
        self.text.setText(random.choice(self.hello))
    def xd(self):
        self.text2.setText("xD")
        
app = QApplication([])
path = Path(__file__).cwd() / "fonts" / "unifont.ttf"
fid = QtGui.QFontDatabase.addApplicationFont(str(path))
app.setFont(QtGui.QFontDatabase.applicationFontFamilies(fid)[0])
widget = App()
widget.resize(800, 600)
widget.show()
with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

sys.exit(app.exec())