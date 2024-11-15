
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout, QProgressBar, QTextEdit, QFileDialog
from PyQt5.QtCore import pyqtSlot
from gui import SampleWorker
from datetime import datetime

class App(QMainWindow):
    def __init__(self, logger):
        super().__init__()
        self.title = 'Website CD Tracklist Maker'
        self.left = 10
        self.top = 10
        self.width = 1024
        self.height = 480
        self.dir_placeholder = "E:/website-cd-tracklist-maker/TestFiles"
        self.logger = logger
        self.initUI()
        
    def initUI(self):
        """ initialize UI window and elements
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # CDs root directory
        self.textbox_cds_dir = QLineEdit(self)
        self.textbox_cds_dir.setText(self.dir_placeholder)
        self.textbox_cds_dir.textChanged.connect(self.set_input_directory)
        
        # Select directory button
        self.button_select = QPushButton('Select CDs Directory', self)
        self.button_select.clicked.connect(self.select_directory)        

        # Select button and directory's horizontal box
        layout_cds_dir = QHBoxLayout()
        layout_cds_dir.addWidget(self.button_select)
        layout_cds_dir.addWidget(self.textbox_cds_dir)
                
        # Progress bar horizontal box
        self.button_start = QPushButton('Start', self)
        self.button_start.clicked.connect(self.confirm_task)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        self.button_stop = QPushButton('Stop', self)
        self.button_stop.setDisabled(True)
        self.button_stop.clicked.connect(self.stop_tasks)

        layout_start_progress = QHBoxLayout()
        layout_start_progress.addWidget(self.button_start)
        layout_start_progress.addWidget(self.progress_bar)
        layout_start_progress.addWidget(self.button_stop)

        self.label_log = QTextEdit()

        # general layout (vertical) box
        layout = QVBoxLayout()
        layout.addLayout(layout_cds_dir)
        layout.addLayout(layout_start_progress)
        layout.addWidget(self.label_log)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.show()
        
    def log(self, new_text):
        """ updates log element with new text line

        Args:
            new_text (str): text line
        """
        txt = self.label_log
        time = datetime.now().strftime("%H:%M:%S")
        txt.append(time +": "+ new_text)
        txt.verticalScrollBar().setValue( txt.verticalScrollBar().maximum() )
    
    def select_directory(self):
        """ opens OS file dialog in order to find the directory with the albums files
        """
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.textbox_cds_dir.setText(dir)
        
    def set_input_directory(self, typed_text):
        """ updates UI directory path component

        Args:
            typed_text (str): typed text
        """
        self.textbox_cds_dir.setText(typed_text)
        
    @pyqtSlot()
    def confirm_task(self):
        """ opens a confirmation popup for the user to confirm the directory before starting the SampleWorker
        """
        cds_dir = self.textbox_cds_dir.text()

        box = QMessageBox()
        return_value = box.question(self, 'Directory confirmation', "Do you confirm this is the correct directory?\n\n" + cds_dir, QMessageBox.No, QMessageBox.Yes)
                
        if(return_value == QMessageBox.No):
            self.logger.info("user not sure, not starting.")
        elif(return_value == QMessageBox.Yes):
            self.start_work()
        else:
            self.logger.info("Where the hell did the user click?")
            
    def signal_log_accept(self, msg):
        """ receives signal from SampleWorker
            appends message to the UI log element
        Args:
            msg (str): text to show on the log element
        """
        self.log(msg)

    def signal_progress_accept(self, percentage_value):
        """ receives signal from SampleWorker
            updates the UI progress bar

        Args:
            percentage_value (int): value between 0-100
        """
        self.progress_bar.setValue(percentage_value)

    def signal_finished_accept(self):
        """ receives signal from SampleWorker
            updates buttons' states.
        """
        self.log("finished.")
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)
        
    def start_work(self):
        """ updates UI and starts SampleWorker thread
        """
        self.button_start.setDisabled(True)
        self.button_stop.setDisabled(False)

        cds_path = self.textbox_cds_dir.text()
        
        self.thread = SampleWorker.SampleWorker(self.logger, cds_path)
        
        self.thread._signal_log.connect(self.signal_log_accept)
        self.thread._signal_progress.connect(self.signal_progress_accept)
        self.thread.finished.connect(self.signal_finished_accept)
        
        self.thread.start()
                    
    def stop_tasks(self):
        """ stops the SampleWorker and updates UI.
        """
        self.thread.stop()
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)