from flask import Flask, render_template, request
from plotting import plot_data
from import_data import load_data, load_file_paths

# Initialisiere die Flask-App
app = Flask(__name__)

# Pfad zu den Dateien und Ordnern
file_paths, folders = load_file_paths()

# Alle Excel-Dateien im Voraus einlesen und in einem Dictionary speichern
datasets = {}
units_data = {}

for file_path, folder in zip(file_paths, folders):
    df, units = load_data(file_path)
    datasets[folder] = df
    units_data[folder] = units

# Hauptseite für Ordner-, X- und Y-Achsen-Auswahl
@app.route('/', methods=['GET', 'POST'])
def select_plot():
    # Ordnerauswahl: Standardmäßig wird der erste Ordner ausgewählt
    selected_folder = request.args.get('folder', folders[0])

    # DataFrame und Units aus dem vorgeladenen Dictionary abrufen
    df = datasets[selected_folder]
    units = units_data[selected_folder]

    # X- und Y-Achsen Auswahl: Standardmäßig die ersten beiden Spalten
    x_col = request.args.get('x_col', df.keys()[0])
    y_col = request.args.get('y_col', df.keys()[1])

    # Plot für die ausgewählten X- und Y-Achsen erstellen
    plot_url = plot_data(df, units, x_col, y_col)

    # HTML-Template rendern mit den Ordnern, X- und Y-Spalten und dem Plot
    return render_template('select_plot.html', folders=folders, selected_folder=selected_folder, x_col=x_col, y_col=y_col, plot_url=plot_url, columns=df.keys())

# Flask starten
if __name__ == '__main__':
    app.run(debug=True)
