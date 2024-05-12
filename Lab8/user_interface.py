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

from ...JezykiSkryptowe.8.ssh_log import SSHLogEntry