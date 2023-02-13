from PySide6.QtWidgets import QLabel, QWidget, QGridLayout, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os, os.path

class Piece:
    stylesheet = """QSpinBox {
  border: 1px solid #ABABAB;
  border-radius: 3px;
}

QSpinBox::down-button  {
  subcontrol-origin: margin;
  subcontrol-position: center left;
  image: url(:/icons/leftArrow.png);
  background-color: #ABABAB;
  left: 1px;
  height: 24px;
  width: 24px;
}

QSpinBox::up-button  {
  subcontrol-origin: margin;
  subcontrol-position: center right;
  image: url(:/icons/rightArrow.png);
  background-color: #ABABAB;
  right: 1px;
  height: 24px;
  width: 24px;
}"""

    widget = None
    part_width = 200
    spinbox = None

    def __init__(self, num, color, img, qty, name):
        self.num = num
        self.name = name
        self.color = color
        self.img = img
        self.qty = qty
        block = QGridLayout()
        block.addWidget(QLabel(self.num + " - " + self.name),0,0,1,2)
        partImage = self.getPixmap()
        partImage.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        block.addWidget(partImage,1,0,3,1)
        quantityLabel = QLabel("Want\n" + str(self.qty))
        quantityLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        block.addWidget(quantityLabel,1,1)
        haveLabel = QLabel("Have")
        haveLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        block.addWidget(haveLabel,2,1)
        self.spinbox = QSpinBox()
        self.spinbox.setMaximum(self.qty)
        self.spinbox.valueChanged.connect(self.spinboxchanged)
        self.spinbox.setStyleSheet(self.stylesheet)
        self.spinbox.setMaximumWidth(100)
        self.spinbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        block.addWidget(self.spinbox,3,1)
        
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: white;")
        self.widget.setBaseSize(80, self.part_width)
        self.widget.setMaximumWidth(self.part_width)
        self.widget.setMinimumWidth(self.part_width)
        self.widget.setLayout(block)

    def getPixmap(self):
        imgicon = QLabel()
        if self.img is not None:
            filepath = os.path.join("images/", str(os.path.basename(self.img)))
            if os.path.exists(filepath):
                image = QPixmap(filepath)
            else:
                image = QPixmap()
        else:
            image = QPixmap()
        imgicon.setPixmap(image)
        imgicon.setMaximumSize(64,64)
        imgicon.setScaledContents(True)
        return imgicon

    def spinboxchanged(self, value_as_int):
        if value_as_int == self.qty:
            self.widget.setStyleSheet("background-color: green;")
        else:
            self.widget.setStyleSheet("background-color: white;")

    def getWidget(self):
        return self.widget