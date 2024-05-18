import sys
from PyQt5.QtWidgets import QApplication
from log_viewer import LogViewer

'''
Cele dydaktyczne
1. Zapoznanie się z adnotacją typami w języku Python.
2. Ćwiczenia związane z pisaniem testów jednostkowych z wykorzystaniem pytest.
Zadania
1. Dokonaj refaktoryzacji części kodów z Laboratorium 6.
Refaktoryzacja powinna obejmować adnotację typami elementów klas:
a. SSHLogJournal,
b. SSHLogEntry i klas pochodnych.
Adnotacji typami powinny zostać poddane wszystkie metody klas w zakresie:
c. parametrów,
d. wartości zwracanych
e. tworzonych zmiennych.
2. Dokonaj statycznej weryfikacji typów z wykorzystaniem narzędzia mypy. Dokonaj
poprawek w kodzie lub adnotacjach w taki sposób, by mypy nie raportował informacji o
błędach.
3. Z wykorzystaniem biblioteki pytest, skonstruuj następujące testy jednostkowe:
a. test weryfikujący poprawność ekstrakcji czasu tworzonego obiektu klasy
SSHLogEntry,
b. testy weryfikujące poprawność ekstrakcji adresu IPv4 (metoda z zad. 1c).
i. test weryfikujący przypadek poprawnego adresu IPv4 w surowej treści
wpisu (np. Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user
webmaster from 173.234.31.186 port 38926 ssh2),
ii. test weryfikujący przypadek niepoprawnie sformułowanego adresu IPv4
(np. Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from
666.777.88.213 port 38926 ssh2)
iii. test weryfikujący brak adresu IP w treści wpisu.
c. test metody append() klasy SSHLogJournal weryfikujący zgodność typu
tworzonego obiektu z założonym typem. Test ten udeokoruj dekoratorem
@pytest.mark.parametrize w taki sposób, by wykorzystać ten test do weryfikacji
zgodności typów związanych z wszystkimi klasami pochodnymi (odrzucenie
hasła, akceptacją hasła, błędem, inną informacją).
'''

def main():            
    app = QApplication(sys.argv)
    
    log_viewer = LogViewer(app)
    log_viewer.show()
    sys.exit(app.exec_())       

if __name__ == "__main__":
    main()