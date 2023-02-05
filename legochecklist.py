import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QSizePolicy, QScrollArea, QVBoxLayout, QSpinBox, QLayout, QLineEdit, QMainWindow
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QRect, QPoint, QMargins, QTimer, QRunnable, Slot, Signal, QObject, QThreadPool
from PySide6 import QtCore, QtGui, QtUiTools
import requests
import json
import os, os.path
from ui_mainwindow import Ui_MainWindow
import traceback

#import urllib.request

part_width = 200
REBRICKABLE_API_KEY = ""
sort_algorithm="name"

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
        spinbox = QSpinBox()
        spinbox.setMaximum(self.qty)
        spinbox.valueChanged.connect(self.spinboxchanged)
        spinbox.setStyleSheet(self.stylesheet)
        spinbox.setMaximumWidth(100)
        spinbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        block.addWidget(spinbox,3,1)
        
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: white;")
        self.widget.setBaseSize(80,part_width)
        self.widget.setMaximumWidth(part_width)
        self.widget.setMinimumWidth(part_width)
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

def sort_by_name(list):
    return list["part"]["name"]

def sort_by_color(list):
    return list["color"]["id"]

def sort_by_partnum(list):
    return list["part"]["part_num"]

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()

class MainWindow(QMainWindow):
    def __init__(self):
        global REBRICKABLE_API_KEY
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.partsLayout = FlowLayout()
            
        self.ui.partsWidget.setLayout(self.partsLayout)

        self.ui.setText.setText("1682-1")
        self.ui.setText.editingFinished.connect(self.setTextChanged)

        self.ui.rebrickableKeyText.setText(REBRICKABLE_API_KEY)
        self.ui.rebrickableKeyText.editingFinished.connect(self.setRebrickableKey)

        self.setTextChanged()

    def setRebrickableKey(self):
        with open('rebrickable.key', 'w') as f:
            f.write(self.ui.rebrickableKeyText.text())

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                # if widget has some id attributes you need to
                # save in a list to maintain order, you can do that here
                # i.e.:   aList.append(widget.someId)
                widget.deleteLater()

    def loadSetInfo(self):
        self.clearLayout(self.partsLayout)
        self.getParts()

    def imagePartsFunction(self, progress_callback):
        set_id = self.ui.setText.text()
        fp = requests.get('https://rebrickable.com/api/v3/lego/sets/' + set_id + '?key=' + REBRICKABLE_API_KEY)
        decoded = json.loads(fp.text)
        fp.close()

        set_name = decoded["name"]
    
        fp = requests.get('https://rebrickable.com/api/v3/lego/sets/' + set_id + '/parts/?page_size=1000&key=' + REBRICKABLE_API_KEY)
        decoded = json.loads(fp.text)
        fp.close()
        
        match (sort_algorithm):
            case 'name': 
                self.sortedresults = sorted(decoded["results"], key=sort_by_name)
            case 'color': 
                self.sortedresults = sorted(decoded["results"], key=sort_by_color)
            case 'partnum': 
                self.sortedresults = sorted(decoded["results"], key=sort_by_partnum)

        progressCount = 0
        for part in self.sortedresults:
            if (part is not None):
                if (part['is_spare'] is not True):
                    if (part["part"]["part_img_url"] != None):
                        if not os.path.exists("images"):
                            os.mkdir("images")
                        if not os.path.exists("images/" + os.path.basename(part["part"]["part_img_url"])):
                            #file doesn't exist, download it
                            r = requests.get(part["part"]["part_img_url"], stream=True)
                            if r.status_code == 200:
                                with open("images/" + os.path.basename(part["part"]["part_img_url"]), 'wb') as f:
                                    f.write(r.content)
            progress_callback.emit(progressCount)
            progressCount += 1
       
        return "Done."

    def progress_fn(self, n):
        self.ui.statusLabel.setText("Caching Image {} of {} from Rebrickable".format(n, len(self.sortedresults)))

    def print_output(self, s):
        self.set_pieces = []
        for part in self.sortedresults:
            if (part['is_spare'] is not True):
                piece = Piece(part["part"]["part_num"], part["color"]["name"], part["part"]["part_img_url"], int(part["quantity"]), part["part"]["name"])
                self.set_pieces.append(piece)
        for part in self.set_pieces:
            self.partsLayout.addWidget(part.getWidget())
        self.ui.statusLabel.setText("Loading Complete from Rebrickable")
        print(s)

    def thread_complete(self):
        print("Image Download Thread Complete.")

    def getParts(self):
        # Pass the function to execute
        worker = Worker(self.imagePartsFunction) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def setTextChanged(self):
        self.ui.statusLabel.setText('Loading...')
        self.loadSetInfo()

def main():
    global REBRICKABLE_API_KEY
    with open('rebrickable.key') as f:
        REBRICKABLE_API_KEY = f.readline().strip()
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()