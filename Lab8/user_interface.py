'''
Laboratorium 8 -Programowanie GUI
w Python
Języki skryptowe
Cele dydaktyczne
1. Zapoznaniesięzprogramowaniemgraficznychinterfejsówużytkownikawjęzyku
Python.
Wprowadzenie
Zadanie z niniejszej listy dotyczy opracowania aplikacji z graficznym interfejsem użytkownika
służącejdoprzeglądanialogów,którabędzieopartaowzorzecmaster-detail.
Master-detail to wzorzec projektowy, który opisuje związek między dwoma zbiorami danych, w
którymjedenznich(master)jestgłównymźródłemdanych,adrugi(detail)jestpowiązanyznim
i zawiera bardziej szczegółowe informacje. W kontekście aplikacji z interfejsem użytkownika,
master-detail jest często stosowanym rozwiązaniem, w ramach którego lista głównych
elementów jest wyświetlana w widoku master, a szczegółowe informacje na temat każdego z
tychelementówsąwyświetlanewwidokudetail.
Zadania
Korzystając z wybranego zestawu narzędzi do programowania GUI oraz programów z
poprzednich list, napiszprogramzinterfejsemgraficznymdoprzeglądanialogówserweraHTTP
lubSSH.Programpowinienbyćwyposażonywnastępującefunkcjonalności:
1. Programpowinienpozwolićnawczytanieplikuzlogami.
2. Powczytaniupliku,programpowinienwyświetlićwierszezapisanewplikuwformielisty.
3. Program powinien implementować wzorzec master-detail w zakresie przeglądania listy
logóworazwyświetlaniaszczegółówdotyczącychkonkretnegologa.
a. Zbiór danych master stanowi lista logów, wyświetlana może być surowa treść
loga,np.uciętado30znakówizakończonawielokropkiem.
1
b. Zbiór danych detail stanowią atrybuty dotyczące konkretnego loga (np. adres
hosta,data,czas,kodstatusu,etc.).
c. Wybranie przez użytkownika loga z listy powinno uaktualnić treści w
komponentachwyświetlającychszczegółydotyczącekonkretnegologa.
4. Program powinien umożliwiać filtrowanie listy logów ze względu na wybrany przedział
czasowy.
5. Program powinien być wyposażony w przyciski “Następny” i “Poprzedni” pozwalające
przeglądać kolejne logi. Zachowanie powiązane z kliknięciem tych przycisków powinno
być równoważne wybraniu przez użytkownika kolejnego/poprzedniego loga. W
przypadkupierwszego/ostatniegologa,przyciskipowinnybyćnieaktywne.
Podczas projektowania aplikacji, zadbaj o to, aby dobrać odpowiednie widżety do wyświetlania
potrzebnych informacji (etykiety/pola tekstowe dla danych tekstowych, pola numeryczne dla
danychliczbowych,polawyborudatydladat.itd.).
Zadbaj o to, aby klasy i funkcje związane z przetwarzaniem logiki aplikacji były odseparowane
odklasifunkcjizwiązanychzinterfejsemużytkownika.
Zaluźnąreferencjęmożeposłużyćponiższyszkic:
'''

from ssh_log import SSHLogEntry
from ssh_log_journal import SSHLogJournal
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton
from pyqt_search_bar import SearchBar

a = SSHLogEntry.create_specific_log("Jan 12 12:12:12 localhost sshd[1234]: Accepted password for root from")       
        
class LogViewer(QMainWindow):
    def __init__(self, dimensions):
        super().__init__()
        self.logs = []
        self.current_log_index = 0
        
        self.setWindowTitle("Log Browser")
        
        self.setGeometry(*dimensions)
        
        self.setup_ui()
        
        self.fill_log_container()
        
    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.search_bar = SearchBar()
        self.search_bar.setPlaceHolder("Input logs file path...")
        self.search_bar.searched.connect(self.search_logs)
        layout.addWidget(self.search_bar)
        
        self.log_list_widget = QListWidget()
        self.log_list_widget.currentRowChanged.connect(self.selected_other_row)
        layout.addWidget(self.log_list_widget)
        
        self.log_details_text_edit = QTextEdit()
        layout.addWidget(self.log_details_text_edit)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_log)
        layout.addWidget(self.next_button)
        
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_log)
        layout.addWidget(self.previous_button)
        
    def fill_log_container(self):
        self.log_list_widget.clear()
        for log in self.logs:
            self.log_list_widget.addItem(log.__repr__()[:30] + "...")
            
        self.change_row_index(0)
            
        self.log_list_widget.setCurrentRow(self.current_log_index)
        
        if len(self.logs) > 0:
            self.change_log(self.current_log_index)
            
    def selected_other_row(self, index):    
        self.change_row_index(index)
        self.display_log()
        
    def change_row_index(self, index):
        self.current_log_index = index
        
        self.previous_button.setEnabled(index != 0)
        self.next_button.setEnabled(index != len(self.logs))
        
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
            
            self.fill_log_container()
        except FileNotFoundError:
            self.search_bar.getSearchBar().setText("File not found. Try again...")
        except ValueError:
            self.search_bar.getSearchBar().setText("Invalid log format. Try again...")
            
            
def set_app_in_centre(app):           
    width = 900
    height = 600
    
    screen_size = app.primaryScreen().size()
    
    x = screen_size.width() // 2 - width // 2
    y = screen_size.height() // 2 - height // 2
    
    return x, y, width, height
            
def gather_logs_from(file_path):    
    journal = SSHLogJournal()
    
    with open(file_path, "r") as f:
        for line in f:
            journal.append(line)
        
    return journal

def main():        
    app = QApplication(sys.argv)
    
    dimensions = set_app_in_centre(app)
    
    log_viewer = LogViewer(dimensions)
    log_viewer.show()
    sys.exit(app.exec_())   
    

if __name__ == "__main__":
    main()