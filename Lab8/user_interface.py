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
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit

a = SSHLogEntry.create_specific_log("Jan 12 12:12:12 localhost sshd[1234]: Accepted password for root from")

def main():   
    file_path = input("Enter file path: ") 
    
    journal = SSHLogJournal()
    
    try:
        with open(file_path, "r") as f:
            for line in f:
                journal.append(line)
    except FileNotFoundError:
        print("File not found!")
        
    for log in journal:
        print(log.__repr__()[:60])
        
        class LogViewer(QMainWindow):
            def __init__(self, logs):
                super().__init__()
                self.logs = logs
                self.current_log_index = 0
                
                self.setWindowTitle("Log Viewer")
                self.setGeometry(100, 100, 500, 400)
                
                self.setup_ui()
                self.display_log()
                
            def setup_ui(self):
                central_widget = QWidget(self)
                self.setCentralWidget(central_widget)
                
                layout = QVBoxLayout(central_widget)
                
                self.log_list_widget = QListWidget()
                self.log_list_widget.currentRowChanged.connect(self.change_log)
                layout.addWidget(self.log_list_widget)
                
                self.log_details_text_edit = QTextEdit()
                layout.addWidget(self.log_details_text_edit)
                
                self.next_button = QPushButton("Next")
                self.next_button.clicked.connect(self.next_log)
                layout.addWidget(self.next_button)
                
                self.previous_button = QPushButton("Previous")
                self.previous_button.clicked.connect(self.previous_log)
                layout.addWidget(self.previous_button)
                
            def display_log(self):
                self.log_list_widget.clear()
                for log in self.logs:
                    self.log_list_widget.addItem(log.__repr__()[:30] + "...")
                    
                self.log_list_widget.setCurrentRow(self.current_log_index)
                self.change_log(self.current_log_index)
                
            def change_log(self, index):
                self.current_log_index = index
                log = self.logs[index]
                self.log_details_text_edit.setPlainText(log.__repr__())
                
            def next_log(self):
                if self.current_log_index < len(self.logs) - 1:
                    self.current_log_index += 1
                    self.log_list_widget.setCurrentRow(self.current_log_index)
                
            def previous_log(self):
                if self.current_log_index > 0:
                    self.current_log_index -= 1
                    self.log_list_widget.setCurrentRow(self.current_log_index)

        def main():
            file_path = input("Enter file path: ")
            
            journal = SSHLogJournal()
            
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        journal.append(line)
            except FileNotFoundError:
                print("File not found!")
            
            app = QApplication(sys.argv)
            log_viewer = LogViewer(journal)
            log_viewer.show()
            sys.exit(app.exec_())

        if __name__ == "__main__":
            main()
    
            
if __name__ == "__main__":
    main()