from flask import Flask, render_template, request
from plotting import plot_data
from import_data import load_data, load_file_paths

# Initialisiere die Flask-App
app = Flask(__name__)

# Pfad zu den Dateien und Ordnern
excel_file_paths, excel_file_names, folders = load_file_paths()

# Alle Excel-Dateien im Voraus einlesen und in einem Dictionary speichern
datasets = {}
units_data = {}

# Verknüpfe Dateinamen mit den Dateipfaden und speichere die Datensätze
for file_path, file_name in zip(excel_file_paths, excel_file_names):
    df, units = load_data(file_path)
    datasets[file_name] = df
    units_data[file_name] = units

# Hauptseite für die Excel-Datei-, X- und Y-Achsen-Auswahl
@app.route('/', methods=['GET', 'POST'])
def select_plot():
    # Excel-Datei-Auswahl: Standardmäßig wird die erste Datei ausgewählt
    selected_file = request.args.get('file', excel_file_names[0])

    # DataFrame und Units aus dem vorgeladenen Dictionary abrufen
    df = datasets[selected_file]
    units = units_data[selected_file]

    # X- und Y-Achsen Auswahl: Standardmäßig die ersten beiden Spalten
    x_col = request.args.get('x_col', df.keys()[0])
    y_col = request.args.get('y_col', df.keys()[1])

    # Plot für die ausgewählten X- und Y-Achsen erstellen
    plot_url = plot_data(df, units, x_col, y_col)

    # HTML-Template rendern mit den Excel-Dateien, X- und Y-Spalten und dem Plot
    return render_template('select_plot.html', files=excel_file_names, selected_file=selected_file,
                           x_col=x_col, y_col=y_col, plot_url=plot_url, columns=df.keys())

# Flask starten
if __name__ == '__main__':
    app.run(debug=True)
