import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool
import requests
import json
import os, os.path

from xml.dom import minidom
from ui_mainwindow import Ui_MainWindow
import traceback

from piece import Piece
from flowlayout import FlowLayout


REBRICKABLE_API_KEY = ""
sort_algorithm="name"

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

class MainWindow(QMainWindow):
    showHaveFlag = True
    showWantedFlag = True

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
        self.ui.actionBoth.triggered.connect(self.showBoth)
        self.ui.actionWanted.triggered.connect(self.showWanted)
        self.ui.actionHave.triggered.connect(self.showHave)
        self.ui.actionExport.triggered.connect(self.exportRebrickableCSV)
        self.ui.actionSave.triggered.connect(self.exportBricklinkXml)
        self.setTextChanged()

    def exportRebrickableCSV(self):
        if not os.path.exists("rebrickable-wantlists"):
            os.mkdir("rebrickable-wantlists")

        filename = "rebrickable-wantlists/" + self.ui.setText.text() + ".csv"
        with open(filename, "w") as f:
            f.write("Part,Color,Quantity\n")
            for part in self.set_pieces:
                if ((part.qty - part.qtyhave) > 0):
                    f.writelines("{},{},{}\n".format(str(part.bricklinkid), str(part.colorid), str(part.qty - part.qtyhave)))


    def exportBricklinkXml(self):
        if not os.path.exists("bricklink-wantlists"):
            os.mkdir("bricklink-wantlists")
        
        root = minidom.Document()
        inventoryNode = root.createElement('INVENTORY')
        root.appendChild(inventoryNode)

        wantedListId = root.createElement('WANTEDLISTID')
        wantedListId.appendChild(root.createTextNode(self.ui.setText.text()))
        inventoryNode.appendChild(wantedListId)
        
        for part in self.set_pieces:
            partChild = root.createElement('ITEM')
            
            node = root.createElement('ITEMTYPE')
            node.appendChild(root.createTextNode("P"))
            partChild.appendChild(node)
            
            node = root.createElement('ITEMID')
            node.appendChild(root.createTextNode(str(part.bricklinkid)))
            partChild.appendChild(node)

            node = root.createElement('COLOR')
            node.appendChild(root.createTextNode(str(part.bricklinkcolorid)))
            partChild.appendChild(node)

            node = root.createElement('MINQTY')
            node.appendChild(root.createTextNode(str(part.qty)))
            partChild.appendChild(node)

            node = root.createElement('QTYFILLED')
            node.appendChild(root.createTextNode(str(part.qtyhave)))
            partChild.appendChild(node)

            inventoryNode.appendChild(partChild)

        filename = "bricklink-wantlists/" + self.ui.setText.text() + ".xml"
        xml_str = root.toprettyxml(indent ="\t") 
        with open(filename, "w") as f:
            f.write(xml_str) 

    def showBoth(self):
        self.ui.actionBoth.setChecked(True)
        self.ui.actionHave.setChecked(False)
        self.ui.actionWanted.setChecked(False)
        for part in self.set_pieces:
            part.widget.show()
    
    def showWanted(self):
        self.ui.actionBoth.setChecked(False)
        self.ui.actionHave.setChecked(False)
        self.ui.actionWanted.setChecked(True)
        for part in self.set_pieces:
            if part.qty != part.spinbox.value():
                part.widget.show()
            else:
                part.widget.hide()

    def showHave(self):
        self.ui.actionBoth.setChecked(False)
        self.ui.actionHave.setChecked(True)
        self.ui.actionWanted.setChecked(False)
        for part in self.set_pieces:
            if part.qty == part.spinbox.value():
                part.widget.show()
            else:
                part.widget.hide()

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
                piece = Piece(part["part"]["part_num"], part["color"]["name"], part["part"]["part_img_url"], int(part["quantity"]), part["part"]["name"], part["color"]["id"],part['part']['external_ids']['BrickLink'][0],part['color']['external_ids']['BrickLink']['ext_ids'][0])
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