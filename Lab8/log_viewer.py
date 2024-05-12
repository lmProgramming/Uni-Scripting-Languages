from pyqt_search_bar import SearchBar
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QLabel, QDateTimeEdit, QCheckBox, QFrame
from PyQt5.QtCore import QDateTime
from ssh_log import SSHLogEntry
from log_reader import gather_logs_from

WIDTH = 900
HEIGHT = 800

ERROR_WIDTH = 300
ERROR_HEIGHT = 200

MAX_TEXT_HEIGHT = 40

LOG_CHAR_LIMIT = 60

SHOW_SPECIFIC_DETAILS = True

class ErrorPopup(QWidget):
    def __init__(self, message, dimensions):
        QWidget.__init__(self)
        
        self.setWindowTitle("Error!")
        
        self.setGeometry(*dimensions)
        
        self.setup_ui(message)        
        
    def setup_ui(self, message):
        layout = QVBoxLayout(self)
        
        label = QLabel(self)
        label.setText(message)
        layout.addWidget(label)
        
        button = QPushButton(self)
        button.setText("Close")
        button.clicked.connect(self.close)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
class LogViewer(QMainWindow):
    def __init__(self, app, dimensions=None):
        super().__init__()
        self.app = app
        self.logs = []
        self.displayed_logs = []
        self.current_log_index = 0       
        
        self.special_details = {}
        
        self.setWindowTitle("Log Browser")
        
        if dimensions is None:
            dimensions = self.get_centre_dimensions(WIDTH, HEIGHT)
        
        self.setGeometry(*dimensions)
        
        self.setMaximumSize(*dimensions[2:])
        
        self.setup_ui()
        
        self.fill_log_container()
        
    def setup_date_layout(self):
        dateLayout = QHBoxLayout()
                
        self.filter_by_date = QCheckBox("Filter by Date: ")
        self.filter_by_date.stateChanged.connect(self.fill_log_container)
        dateLayout.addWidget(self.filter_by_date)        
        
        self.from_date_edit = QDateTimeEdit()
        self.from_date_edit.setCalendarPopup(True)
        self.from_date_edit.dateTimeChanged.connect(self.fill_log_container)        
        dateLayout.addWidget(self.from_date_edit)
                
        self.to_date_edit = QDateTimeEdit()
        self.to_date_edit.setCalendarPopup(True)
        self.to_date_edit.dateTimeChanged.connect(self.fill_log_container)      
        dateLayout.addWidget(self.to_date_edit)
        
        return dateLayout
    
    def setup_main_layout(self):
        mainLayout = QHBoxLayout()
        
        mainLayout.addLayout(self.setup_log_list_layout(), 60)        
        mainLayout.addLayout(self.setup_details_layout(), 40)
        
        return mainLayout
    
    def create_text_with_label(self, label_text):
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        layout.addWidget(label)
        
        text = QTextEdit()   
        text.setReadOnly(True)     
        text.setMaximumHeight(MAX_TEXT_HEIGHT)
        
        layout.addWidget(text)
        
        return layout, text
    
    def setup_details_layout(self):
        detailsLayout = QVBoxLayout()
        
        self.details_label = QLabel("Details:")
        detailsLayout.addWidget(self.details_label)       
        
        layout, self.unparsed_details_text = self.create_text_with_label("Unparsed details")
        detailsLayout.addLayout(layout)
        
        layout, self.server_name_text = self.create_text_with_label("Server name")
        detailsLayout.addLayout(layout)
        
        layout, self.event_text = self.create_text_with_label("Event")
        detailsLayout.addLayout(layout)
        
        layout, self.user_text = self.create_text_with_label("User")
        detailsLayout.addLayout(layout)
        
        layout, self.ipv4_text = self.create_text_with_label("IPV4")
        detailsLayout.addLayout(layout)
        
        layout, self.message_text = self.create_text_with_label("Message")
        detailsLayout.addLayout(layout)
        
        self.create_special_details_text(detailsLayout, "Port", "port")
        self.create_special_details_text(detailsLayout, "SSH type", "ssh_type")
        self.create_special_details_text(detailsLayout, "Error type", "error")     
        
        self.details_layout = detailsLayout
        
        return detailsLayout

    def create_special_details_text(self, detailsLayout, label_text, key):
        frame = QFrame()
        
        layout, port_text = self.create_text_with_label(label_text)
        frame.setLayout(layout)    
        frame.setContentsMargins(0, 0, 0, 0)   
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame.hide()
        self.special_details[key] = (frame, port_text)        
        
        detailsLayout.addWidget(frame)
    
    def setup_log_list_layout(self):
        logListLayout = QVBoxLayout()
        
        self.log_list_label = QLabel("Logs:")
        logListLayout.addWidget(self.log_list_label)
        
        self.log_list_widget = QListWidget()
        self.log_list_widget.itemSelectionChanged.connect(lambda: self.selected_other_row(self.log_list_widget.currentRow()))
        logListLayout.addWidget(self.log_list_widget)
        
        return logListLayout
        
    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
               
        self.search_bar = SearchBar()
        self.search_bar.setPlaceHolder("Input logs file path...")
        self.search_bar.searched.connect(self.search_logs)
        layout.addWidget(self.search_bar)
                        
        layout.addLayout(self.setup_date_layout())        
        
        layout.addLayout(self.setup_main_layout())               
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_log)
        layout.addWidget(self.next_button)
        
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_log)
        layout.addWidget(self.previous_button)
        
    def fill_log_container(self):
        self.log_list_widget.clear()
        
        self.displayed_logs = self.filter_logs_by_date()
        
        for log in self.displayed_logs:
            self.log_list_widget.addItem(log.__repr__()[:LOG_CHAR_LIMIT] + "...")
            
        self.change_row_index(0)
            
        self.log_list_widget.setCurrentRow(self.current_log_index)
        
        if len(self.logs) > 0:
            self.change_log(self.current_log_index)
            
    def show_error_popup(self, message):
        self.error_popup = ErrorPopup(message, self.get_centre_dimensions(ERROR_WIDTH, ERROR_HEIGHT))
        self.error_popup.show()
            
    def selected_other_row(self, index):    
        self.change_row_index(index)
        self.display_log()
        
    def change_row_index(self, index):
        self.current_log_index = index
        
        self.previous_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.displayed_logs) - 1 or len(self.displayed_logs) == 0)
        
    def display_log(self):            
        self.log_list_widget.setCurrentRow(self.current_log_index)
        
        self.change_log(self.current_log_index)
        
    def change_log(self, index):
        self.current_log_index = index
        log = self.logs[index]
        
        self.update_log_details(log)
        
    def update_log_details(self, log: SSHLogEntry):
        self.unparsed_details_text.setPlainText(str(log.details))
        self.server_name_text.setPlainText(str(log.server_name))
        self.event_text.setPlainText(str(log.event))
        self.user_text.setPlainText(str(log.user))
        self.ipv4_text.setPlainText(str(log.ipv4))
        self.message_text.setPlainText(str(log.message))
        
        if SHOW_SPECIFIC_DETAILS:
            self.update_special_details(log)
        
    def update_special_details(self, log: SSHLogEntry):
        for key, (frame, text) in self.special_details.items():
            if hasattr(log, key):
                text.setPlainText(str(getattr(log, key)))
                frame.show()
            else:
                frame.hide()
        
    def next_log(self):
        if self.current_log_index < len(self.logs) - 1:
            self.change_row_index(self.current_log_index + 1)
            self.log_list_widget.setCurrentRow(self.current_log_index)
        
    def previous_log(self):
        if self.current_log_index > 0:
            self.change_row_index(self.current_log_index - 1)
            self.log_list_widget.setCurrentRow(self.current_log_index)
            
    def search_logs(self, file_path):    
        try:
            self.logs = gather_logs_from(file_path)         
            self.fill_log_container()          
            return
        except FileNotFoundError:
            error_message = "File not found. Try again..."             
        except ValueError:
            error_message = "Invalid log format. Try again..."
            
        self.search_bar.getSearchBar().setText(error_message)            
        self.show_error_popup(error_message)
            
    def filter_logs_by_date(self):
        if not self.filter_by_date.isChecked():
            return self.logs
        
        from_date = self.from_date_edit.dateTime().toPyDateTime()
        to_date = self.to_date_edit.dateTime().toPyDateTime()
        
        return [log for log in self.logs if from_date <= log.timestamp <= to_date]   
    
    def get_centre_dimensions(self, width, height):   
        primary_screen_dimensions = self.app.primaryScreen().size()  
            
        x = primary_screen_dimensions.width() // 2 - width // 2
        y = primary_screen_dimensions.height() // 2 - height // 2
        
        return x, y, width, height
      