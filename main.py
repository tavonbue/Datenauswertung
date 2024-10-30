from flask import Flask, render_template, request, send_file
from plotting import plot_data
from import_data import load_file_paths, load_dataframe

from io import BytesIO
import pickle
from datetime import datetime
app = Flask(__name__)

# Pfad zu den Dateien und Ordnern
excel_file_paths, excel_file_names, folders = load_file_paths()

# Alle Excel-Dateien im Voraus einlesen und in einem Dictionary speichern
datasets = {}
units_data = {}

# Verknüpfe Dateinamen mit den Dateipfaden und speichere die Datensätze
for file_path, file_name in zip(excel_file_paths, excel_file_names):
    df, units = load_dataframe(file_path)
    datasets[file_name] = df
    units_data[file_name] = units

# Hilfsfunktion, um Eingabewerte als float oder None zu verarbeiten
def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

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

    # Minimal- und Maximalwerte sowie Schrittweiten für X- und Y-Achsen
    x_min = parse_float(request.args.get('x_min'))
    x_max = parse_float(request.args.get('x_max'))
    y_min = parse_float(request.args.get('y_min'))
    y_max = parse_float(request.args.get('y_max'))
    x_step = parse_float(request.args.get('x_step'))
    y_step = parse_float(request.args.get('y_step'))

    # Plot für die ausgewählten X- und Y-Achsen erstellen
    plot_url = plot_data(
        df, units, x_col, y_col,
        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
        x_step=x_step, y_step=y_step
    )

    # HTML-Template rendern
    return render_template('select_plot.html', files=excel_file_names, selected_file=selected_file,
                           x_col=x_col, y_col=y_col, plot_url=plot_url, columns=df.keys(),
                           x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                           x_step=x_step, y_step=y_step)

# Route für den PDF-Download
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    # Formulardaten abrufen
    selected_file = request.form.get('file')
    x_col = request.form.get('x_col')
    y_col = request.form.get('y_col')
    x_min = parse_float(request.form.get('x_min'))
    x_max = parse_float(request.form.get('x_max'))
    y_min = parse_float(request.form.get('y_min'))
    y_max = parse_float(request.form.get('y_max'))
    x_step = parse_float(request.form.get('x_step'))  # Schrittweite X abrufen
    y_step = parse_float(request.form.get('y_step'))  # Schrittweite Y abrufen

    # Daten abrufen und den Plot als PDF erstellen
    df = datasets[selected_file]
    units = units_data[selected_file]

    pdf_bytes = plot_data(df, units, x_col, y_col, x_min, x_max, y_min, y_max, x_step, y_step, output_format='pdf')

    # Dynamischer Dateiname basierend auf der Auswahl
    pdf_filename = f"{selected_file.split('.')[0]}_{x_col}_vs_{y_col}.pdf"

    # Sendet die PDF-Datei an den Benutzer
    return send_file(pdf_bytes, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')




if __name__ == '__main__':
    app.run(debug=True)
