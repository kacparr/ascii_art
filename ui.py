import random
import sys
import string
import random
from pathlib import Path
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *


class WindowBar(QWidget):
    def __init__(self, parent) :
        super().__init__(parent)
        self.setFixedSize(800,30)
        layout = QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(1, 1, 1, 1)
        #icons
        self.icon = QLabel()
        self.icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.movie = QtGui.QMovie(self.getIcon())
        self.icon.setMovie(self.movie)
        self.movie.start()
        #title
        self.title = QLabel("Asciify your art!")
        self.title.setStyleSheet("font-weight: bold;")
        #buttons
        self.button_min = QPushButton()
        self.button_min.setIcon(QtGui.QIcon("./assets/icons/bar/min.png"))
        self.button_min.clicked.connect(self.window().showMinimized)
        self.button_close = QPushButton()
        self.button_close.setIcon(QtGui.QIcon("./assets/icons/bar/close.png"))
        self.button_close.clicked.connect(self.window().close)
        buttons = [self.button_min,self.button_close]
        for button in buttons:
            button.setFixedSize(30,30)
            button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        #widgets    
        self.spacer = QSpacerItem(self.x() - self.icon.x() - self.title.x() - self.button_min.x() - self.button_close.x(),16,QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addSpacerItem(self.spacer)
        layout.addWidget(self.button_min)
        layout.addWidget(self.button_close)
        self.setLayout(layout)

        self.offset = None
    
    def paintEvent(self,e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('#000181'))
        brush.setStyle(QtCore.Qt.SolidPattern)
        bar = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())            
        painter.fillRect(bar, brush)
        
    def sizeHint(self):
        return QtCore.QSize(1,1)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
        event.accept()
    
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self.offset)
        event.accept()
    
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.offset = None
        event.accept()
    
 
    def getIcon(self):
        path = Path(__file__).cwd() / "assets" / "icons"
        items = [str(path) for path in path.iterdir()]
        return random.choice(items)

class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ASCII Generator")
        self.setFixedSize(800,600)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.FramelessWindowHint)
        
        
        self.hello = ["Siemaneczko", "eluwina"]
        with open("pa2.hex","r") as f:
            self.palette = [x.strip() for x in f.readlines()]
        self.letter_table = [x for x in string.printable]
        self.letters = [self.create_letter(random.choice(self.letter_table)) for _ in range(150)]
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(25)
        
        
        window_layout = QVBoxLayout()
        self.setLayout(window_layout)
        window_layout.setContentsMargins(0,0,0,0)
        self.windowbar = WindowBar(self)
        window_layout.addWidget(self.windowbar)
        
        self.main_widget = QStackedWidget()
        window_layout.addWidget(self.main_widget)
        
        self.start_widget = QWidget()
        self.init_start_widget()

        
        self.image_widget = QWidget()
        self.init_image_widget()
        
        self.select_image_widget = QWidget()
        
        self.main_widget.addWidget(self.start_widget)
        self.main_widget.addWidget(self.image_widget)
        self.main_widget.addWidget(self.select_image_widget)
        self.main_widget.setCurrentWidget(self.start_widget)

        
        
    def init_start_widget(self):
        layout = QVBoxLayout()
        self.start_widget.setLayout(layout)
        self.text = QLabel("Select your desired output.")   
        self.text.setStyleSheet("font-size: 20px")
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button_text = QPushButton("Text")
        self.button_text.setFixedSize(350,50)
        self.button_image = QPushButton("Image")
        self.button_image.setFixedSize(350,50)
        self.button_image.clicked.connect(self.show_image_widget)
        button_layout.addWidget(self.button_text)
        button_layout.addWidget(self.button_image)
        
        layout.addWidget(self.text)
        layout.addLayout(button_layout)

    def init_image_widget(self):
        layout = QVBoxLayout()
        self.image_widget.setLayout(layout)
        self.text = QLabel("Select the type of image.")
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.text.setStyleSheet("font-size: 20px")


        images_layout = QHBoxLayout()
        images_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.image1 = QLabel()
        self.image1.setPixmap(QtGui.QPixmap("./assets/img/res.png").scaled(350,450))
        
        self.image2 = QLabel()
        self.movie = QtGui.QMovie("./assets/img/pes_animated.gif")
        self.movie.setScaledSize(QtCore.QSize(350,450))
        self.image2.setMovie(self.movie)
        self.movie.start()
        images_layout.addWidget(self.image1)
        images_layout.addWidget(self.image2)
        
        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button_standard = QPushButton("Standard")
        self.button_standard.setFixedSize(350,50)
        self.button_animated = QPushButton("Animated")
        self.button_animated.setFixedSize(350,50)
        button_layout.addWidget(self.button_standard)
        button_layout.addWidget(self.button_animated)
        
        layout.addWidget(self.text)
        layout.addLayout(images_layout)
        layout.addLayout(button_layout)
    
    def init_select_image_widget(self):
        layout = QVBoxLayout()
        self.image_widget.setLayout(layout)
        self.text = QLabel("Select the type of image.")
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.text.setStyleSheet("font-size: 20px")


        images_layout = QHBoxLayout()
        images_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.image1 = QLabel()
        self.image1.setPixmap(QtGui.QPixmap("./assets/img/res.png").scaled(350,450))
        
        self.image2 = QLabel()
        self.movie = QtGui.QMovie("./assets/img/pes_animated.gif")
        self.movie.setScaledSize(QtCore.QSize(350,450))
        self.image2.setMovie(self.movie)
        self.movie.start()
        images_layout.addWidget(self.image1)
        images_layout.addWidget(self.image2)
        
        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button_standard = QPushButton("Standard")
        self.button_standard.setFixedSize(350,50)
        self.button_animated = QPushButton("Animated")
        self.button_animated.setFixedSize(350,50)
        button_layout.addWidget(self.button_standard)
        button_layout.addWidget(self.button_animated)
        
        layout.addWidget(self.text)
        layout.addLayout(images_layout)
        layout.addLayout(button_layout)
    def show_image_widget(self):
        self.main_widget.setCurrentWidget(self.image_widget)
        
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
fontPath = Path(__file__).cwd() / "fonts" / "unifont.ttf"
fid = QtGui.QFontDatabase.addApplicationFont(str(fontPath))
app.setFont(QtGui.QFontDatabase.applicationFontFamilies(fid)[0])
widget = App()
widget.resize(800, 600)
widget.show()
with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

sys.exit(app.exec())