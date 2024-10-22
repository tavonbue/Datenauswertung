# Datenauswertung
Versuchsdaten auswerten und plotten

Überblick
Diese Flask-basierte Webanwendung ermöglicht es, Excel-Dateien aus mehreren Ordnern zu laden, deren Spalten zu visualisieren und dynamische Plots zu erstellen. Der Benutzer kann aus verschiedenen Ordnern eine Excel-Datei auswählen, die Spalten für die X- und Y-Achsen festlegen und einen entsprechenden Plot generieren. Die Anwendung wurde optimiert, um alle Excel-Daten im Voraus einzulesen und im Speicher abzulegen, um so eine flüssigere Benutzererfahrung zu gewährleisten.

Funktionen
Auswahl eines Ordners mit einer Excel-Datei über ein Dropdown-Menü.
Dynamische Auswahl von X- und Y-Achsen aus den Spalten der geladenen Excel-Datei.
Echtzeit-Generierung von Plots basierend auf den ausgewählten Daten.
Schnelle Leistung durch vorgeladenen Excel-Datensätze.
Ordnerstruktur
Jeder Ordner enthält eine Excel-Datei, die von der App geladen wird. Die Excel-Dateien werden im Voraus in einem Dictionary gespeichert, um unnötige Lesevorgänge von der Festplatte zu vermeiden.

Verwendete Technologien
Python: Programmiersprache für das Backend.
Flask: Web-Framework für die Erstellung der Webanwendung.
Pandas: Für das Laden und Verarbeiten der Excel-Daten.
Matplotlib: Für die Erstellung der Plots.
HTML/CSS: Für das Layout und die Benutzeroberfläche der Web-App.
Installation
Klone das Repository:

bash
Code kopieren
git clone <repository-url>
Navigiere in das Verzeichnis:

bash
Code kopieren
cd excel-plotter-app
Installiere die benötigten Python-Abhängigkeiten:

bash
Code kopieren
pip install -r requirements.txt
Stelle sicher, dass die Ordnerstruktur mit den Excel-Dateien wie gewünscht konfiguriert ist. Jede Excel-Datei sollte sich in einem separaten Ordner befinden.

Verwendung
Starte die Flask-App:

bash
Code kopieren
python app.py
Öffne deinen Browser und rufe die Web-App unter http://127.0.0.1:5000 auf.

Wähle im ersten Dropdown-Menü den gewünschten Ordner aus.

Wähle im zweiten und dritten Dropdown-Menü die Spalten für die X- und Y-Achsen aus.

Der entsprechende Plot wird dynamisch generiert und angezeigt.

Anpassungen
Du kannst die Struktur und die Namen der Ordner und Dateien anpassen, indem du die Funktion load_file_paths() entsprechend änderst.
Zusätzliche Plot-Optionen können leicht durch Modifikationen in der Funktion plot_data() implementiert werden.
Beispiele
Wenn du einen Ordner mit einer Excel-Datei wie folgt hast:

plaintext
Code kopieren
Ordner1/
  └── daten1.xlsx
Ordner2/
  └── daten2.xlsx
Die Web-App erkennt diese Struktur und lädt die Excel-Dateien entsprechend. Du kannst dann auswählen, welche Spalten geplottet werden sollen.

Kontakt
Bei Fragen oder Feedback wende dich bitte an [deine E-Mail-Adresse].
