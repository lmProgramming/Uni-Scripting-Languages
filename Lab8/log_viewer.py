from pyqt_search_bar import SearchBar
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QLabel, QDateTimeEdit
from log_reader import gather_logs_from

WIDTH = 900
HEIGHT = 600

ERROR_WIDTH = 300
ERROR_HEIGHT = 200

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
        self.current_log_index = 0
        
        self.setWindowTitle("Log Browser")
        
        if dimensions is None:
            dimensions = self.get_centre_dimensions(WIDTH, HEIGHT)
        
        self.setGeometry(*dimensions)
        
        self.setup_ui()
        
        self.fill_log_container()
        
    def setup_date_layout(self):
        dateLayout = QHBoxLayout()
        
        self.date_label = QLabel("Filter by Date:")
        dateLayout.addWidget(self.date_label)
        
        self.from_date_edit = QDateTimeEdit()
        self.from_date_edit.setCalendarPopup(True)
        dateLayout.addWidget(self.from_date_edit)
                
        self.to_date_edit = QDateTimeEdit()
        self.to_date_edit.setCalendarPopup(True)
        dateLayout.addWidget(self.to_date_edit)
        
        return dateLayout
    
    def setup_main_layout(self):
        mainLayout = QHBoxLayout()
        
        mainLayout.addLayout(self.setup_log_list_layout(), 60)        
        mainLayout.addLayout(self.setup_details_layout())
        
        return mainLayout
    
    def setup_details_layout(self):
        detailsLayout = QVBoxLayout()
        
        self.details_label = QLabel("Details:")
        detailsLayout.addWidget(self.details_label)
        
        self.details_text_edit = QTextEdit()
        detailsLayout.addWidget(self.details_text_edit)
        
        return detailsLayout
    
    def setup_log_list_layout(self):
        logListLayout = QVBoxLayout()
        
        self.log_list_label = QLabel("Logs:")
        logListLayout.addWidget(self.log_list_label)
        
        self.log_list_widget = QListWidget()
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
        for log in self.filter_logs_by_date():
            self.log_list_widget.addItem(log.__repr__()[:30] + "...")
            
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
        self.next_button.setEnabled(index < len(self.logs) - 1 or len(self.logs) == 0)
        
    def display_log(self):            
        self.log_list_widget.setCurrentRow(self.current_log_index)
        
        self.change_log(self.current_log_index)
        
    def change_log(self, index):
        self.current_log_index = index
        log = self.logs[index]
        self.log_details_text_edit.setPlainText(log.__repr__())
        
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
            self.filter_logs_by_date()
            self.fill_log_container()
            return
        except FileNotFoundError:
            error_message = "File not found. Try again..."             
        except ValueError:
            error_message = "Invalid log format. Try again..."
            
        self.search_bar.getSearchBar().setText(error_message)            
        self.show_error_popup(error_message)
            
    def filter_logs_by_date(self):
        from_date = self.from_date_edit.date().toPyDate()
        to_date = self.to_date_edit.date().toPyDate()
        
        return [log for log in self.logs if from_date <= log.timestamp <= to_date]   
    
    def get_centre_dimensions(self, width, height):   
        primary_screen_dimensions = self.app.primaryScreen().size()  
            
        x = primary_screen_dimensions.width() // 2 - width // 2
        y = primary_screen_dimensions.height() // 2 - height // 2
        
        return x, y, width, height
      