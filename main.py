from flask import Flask, render_template, request, send_file
from plotting import plot_data, plotly_interactive_plot
from import_data import load_file_paths, load_dataframe
from io import BytesIO
import pandas as pd
import os

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

# Hilfsfunktion, um Eingabewerte als Datum oder None zu verarbeiten
def parse_date(value):
    try:
        return pd.to_datetime(value)
    except (TypeError, ValueError):
        return None

# Preprocessing-Seite zum Bearbeiten und Beschneiden des DataFrames
@app.route('/', methods=['GET', 'POST'])
def preprocessing():
    selected_file = request.args.get('file', excel_file_names[0])

    # Prüfen, ob ein bearbeiteter DataFrame existiert
    processed_file_path = f'processed_{selected_file}.pkl'
    if os.path.exists(processed_file_path):
        df = pd.read_pickle(processed_file_path)
    else:
        df = datasets[selected_file]  # Original-DataFrame laden

    units = units_data[selected_file]

    # X-Achse immer die erste Spalte (Sekunden), Y-Achse wird ausgewählt
    x_col = df.columns[0]  # Die X-Achse bleibt immer die erste Spalte
    y_col = request.args.get('y_col', df.columns[1])

    # Konvertiere die Werte der X-Achse (erste Spalte) in float, falls sie als 'object' formatiert sind
    try:
        df[x_col] = df[x_col].astype(float)
    except ValueError as e:
        print(f"Fehler bei der Konvertierung von {x_col} zu float: {e}")

    # Überprüfe, ob der Reset-Button gedrückt wurde
    reset_x_axis = request.args.get('reset_x_axis')
    if reset_x_axis:
        # Lade den ursprünglichen DataFrame ohne Bearbeitung
        df_processed = datasets[selected_file]
        x_max_input = None  # Setze x_max_input auf None
    else:
        # Maximalwert für die X-Achse (Sekunden) aus dem Eingabefeld
        x_max_input = request.args.get('x_max')
        df_processed = df

        if x_max_input and x_max_input.lower() != 'none':
            try:
                # Versuche, die Eingabe als float zu konvertieren
                x_max = float(x_max_input)
                # Beschneide den DataFrame basierend auf der X-Achse (Sekunden)
                df_processed = df[df[x_col] <= x_max]
            except ValueError as e:
                print(f"Fehler bei der Konvertierung von x_max: {e}")
        else:
            # Wenn x_max_input nicht gesetzt oder 'None' ist, verwende den ursprünglichen DataFrame
            df_processed = df

    # Speichere den bearbeiteten DataFrame als Pickle-Datei
    df_processed.to_pickle(processed_file_path)

    # Erstelle den interaktiven Plot mit dem bearbeiteten DataFrame
    plot_html = plotly_interactive_plot(
        df_processed, units, x_col, y_col
    )

    return render_template('preprocessing.html', files=excel_file_names, selected_file=selected_file,
                           x_col=x_col, y_col=y_col, plot_html=plot_html, columns=df.columns,
                           x_max=x_max_input)


# Hilfsfunktion, um Eingabewerte als Datum oder None zu verarbeiten
def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# Hauptseite für die Excel-Datei-, X- und Y-Achsen-Auswahl (Post-Processing)
@app.route('/postprocessing', methods=['GET', 'POST'])
def postprocessing():
    selected_file = request.args.get('file', excel_file_names[0])

    # Versuche, den verarbeiteten DataFrame zu laden, ansonsten den Originalen verwenden
    try:
        df = pd.read_pickle(f'processed_{selected_file}.pkl')
    except FileNotFoundError:
        df = datasets[selected_file]
    units = units_data[selected_file]

    # X- und Y-Achsen Auswahl
    x_col = request.args.get('x_col', df.columns[0])
    y_col = request.args.get('y_col', df.columns[1])

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

    return render_template('postprocessing.html', files=excel_file_names, selected_file=selected_file,
                           x_col=x_col, y_col=y_col, plot_url=plot_url, columns=df.columns,
                           x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                           x_step=x_step, y_step=y_step)



# Route für den PDF-Download
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    selected_file = request.form.get('file', excel_file_names[0])

    try:
        df = pd.read_pickle(f'processed_{selected_file}.pkl')
    except FileNotFoundError:
        df = datasets[selected_file]
    units = units_data[selected_file]

    # X- und Y-Achsen Auswahl
    x_col = request.form.get('x_col', df.columns[0])
    y_col = request.form.get('y_col', df.columns[1])

    # Minimal- und Maximalwerte sowie Schrittweiten für X- und Y-Achsen
    x_min = parse_float(request.form.get('x_min'))
    x_max = parse_float(request.form.get('x_max'))
    y_min = parse_float(request.form.get('y_min'))
    y_max = parse_float(request.form.get('y_max'))
    x_step = parse_float(request.form.get('x_step'))
    y_step = parse_float(request.form.get('y_step'))

    # Daten abrufen und den Plot als PDF erstellen
    pdf_bytes = plot_data(
        df, units, x_col, y_col, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
        x_step=x_step, y_step=y_step, output_format='pdf'
    )

    # Dynamischer Dateiname basierend auf der Auswahl
    pdf_filename = f"{selected_file.split('.')[0]}_{y_col}.pdf"

    return send_file(pdf_bytes, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
