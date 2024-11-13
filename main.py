import io
from flask import Flask, render_template, request, send_file, jsonify, session
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from plotting import plot_data, plotly_interactive_plot, plot_data_with_subplots, plot_data_with_traces
from import_data import load_file_paths, load_dataframe
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Notwendig für die Verwendung von Sessions

# Pfad zu den Dateien und Ordnern
excel_file_paths, excel_file_names, folders = load_file_paths()

# Erstelle die Ordner "Processed_data" und "PDF_Export", falls sie nicht existieren
if not os.path.exists("Processed_data"):
    os.makedirs("Processed_data")
if not os.path.exists("PDF_Export"):
    os.makedirs("PDF_Export")

# Alle Excel-Dateien im Voraus einlesen und in einem Dictionary speichern
datasets = {}
units_data = {}

# Verknüpfe Dateinamen mit den Dateipfaden und speichere die Datensätze
for file_path, file_name in zip(excel_file_paths, excel_file_names):
    df, units = load_dataframe(file_path)
    datasets[file_name] = df
    units_data[file_name] = units

# Preprocessing-Seite zum Bearbeiten und Beschneiden des DataFrames
@app.route('/', methods=['GET', 'POST'])
def preprocessing():
    selected_file = request.args.get('file', excel_file_names[0])
    processed_file_path = os.path.join("Processed_data", f'processed_{selected_file}.pkl')

    # Prüfe, ob der bearbeitete DataFrame existiert
    if os.path.exists(processed_file_path):
        df = pd.read_pickle(processed_file_path)
    else:
        df = datasets[selected_file]

    units = units_data[selected_file]
    x_col = df.columns[0]
    y_col = request.args.get('y_col', df.columns[1])

    try:
        df[x_col] = df[x_col].astype(float)
    except ValueError as e:
        print(f"Fehler bei der Konvertierung von {x_col} zu float: {e}")

    reset_x_axis = request.args.get('reset_x_axis')
    x_max_input = request.args.get('x_max')
    df_processed = df

    if reset_x_axis:
        df_processed = datasets[selected_file]
        x_max_input = None
    elif x_max_input and x_max_input.lower() != 'none':
        try:
            x_max = float(x_max_input)
            df_processed = df[df[x_col] <= x_max]
        except ValueError as e:
            print(f"Fehler bei der Konvertierung von x_max: {e}")

    # Speichere den bearbeiteten DataFrame im Ordner "Processed_data"
    df_processed.to_pickle(processed_file_path)

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
    # Spur 1
    selected_file1 = request.args.get('file1', excel_file_names[0])
    df1 = pd.read_pickle(os.path.join("Processed_data", f'processed_{selected_file1}.pkl'))
    units = units_data[selected_file1]
    x_col1 = request.args.get('x_col1', df1.columns[0])
    y_col1 = request.args.get('y_col1', df1.columns[1])

    # Spur 2
    selected_file2 = request.args.get('file2', excel_file_names[0])
    df2 = pd.read_pickle(os.path.join("Processed_data", f'processed_{selected_file2}.pkl'))
    x_col2 = request.args.get('x_col2', df2.columns[0])
    y_col2 = request.args.get('y_col2', df2.columns[1])

    # Spur 3
    selected_file3 = request.args.get('file3', excel_file_names[0])
    df3 = pd.read_pickle(os.path.join("Processed_data", f'processed_{selected_file3}.pkl'))
    x_col3 = request.args.get('x_col3', df3.columns[0])
    y_col3 = request.args.get('y_col3', df3.columns[1])

    # Achsengrenzen und Schrittweiten
    x_min = parse_float(request.args.get('x_min'))
    x_max = parse_float(request.args.get('x_max'))
    y_min = parse_float(request.args.get('y_min'))
    y_max = parse_float(request.args.get('y_max'))
    x_step = parse_float(request.args.get('x_step'))
    y_step = parse_float(request.args.get('y_step'))

    # Checkboxes für Ein-/Ausblenden der Spuren
    show_curve2 = request.args.get('show_curve2') == 'on'
    show_curve3 = request.args.get('show_curve3') == 'on'

    # Erstelle den Plot
    plot_url = plot_data_with_traces(
        df1, units, x_col1, y_col1, df2 if show_curve2 else None,
        x_col2, y_col2, df3 if show_curve3 else None, x_col3, y_col3,
        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
        x_step=x_step, y_step=y_step, output_format='png'
    )

    return render_template('postprocessing.html',
                           files=excel_file_names,
                           selected_file1=selected_file1, x_col1=x_col1, y_col1=y_col1,
                           selected_file2=selected_file2, x_col2=x_col2, y_col2=y_col2,
                           selected_file3=selected_file3, x_col3=x_col3, y_col3=y_col3,
                           columns=df1.columns,  # Hier sicherstellen, dass Spalten übergeben werden
                           x_min=x_min, x_max=x_max, x_step=x_step,
                           y_min=y_min, y_max=y_max, y_step=y_step,
                           show_curve2=show_curve2, show_curve3=show_curve3,  # Übergabe der Checkbox-Zustände
                           plot_url=plot_url)



# Route für das Rendering der Subplots-Seite
@app.route('/subplots', methods=['GET', 'POST'])
def subplots():
    # Einstellungen für den ersten Plot
    selected_file1 = request.args.get('file1', excel_file_names[0])
    processed_file_path1 = os.path.join("Processed_data", f'processed_{selected_file1}.pkl')

    try:
        df1 = pd.read_pickle(processed_file_path1)
    except FileNotFoundError:
        df1 = datasets[selected_file1]
    units1 = units_data[selected_file1]

    x_col1 = request.args.get('x_col1', df1.columns[0])
    y_col1 = request.args.get('y_col1', df1.columns[1])
    x_min1 = parse_float(request.args.get('x_min1'))
    x_max1 = parse_float(request.args.get('x_max1'))
    y_min1 = parse_float(request.args.get('y_min1'))
    y_max1 = parse_float(request.args.get('y_max1'))
    x_step1 = parse_float(request.args.get('x_step1'))
    y_step1 = parse_float(request.args.get('y_step1'))

    # Erstelle den ersten Plot
    plot_url1 = plot_data(
        df1, units1, x_col1, y_col1,
        x_min=x_min1, x_max=x_max1, y_min=y_min1, y_max=y_max1,
        x_step=x_step1, y_step=y_step1, n_plots=2
    )

    # Einstellungen für den zweiten Plot
    selected_file2 = request.args.get('file2', excel_file_names[0])
    processed_file_path2 = os.path.join("Processed_data", f'processed_{selected_file2}.pkl')

    try:
        df2 = pd.read_pickle(processed_file_path2)
    except FileNotFoundError:
        df2 = datasets[selected_file2]
    units2 = units_data[selected_file2]

    x_col2 = request.args.get('x_col2', df2.columns[0])
    y_col2 = request.args.get('y_col2', df2.columns[1])
    x_min2 = parse_float(request.args.get('x_min2'))
    x_max2 = parse_float(request.args.get('x_max2'))
    y_min2 = parse_float(request.args.get('y_min2'))
    y_max2 = parse_float(request.args.get('y_max2'))
    x_step2 = parse_float(request.args.get('x_step2'))
    y_step2 = parse_float(request.args.get('y_step2'))

    # Erstelle den zweiten Plot
    plot_url2 = plot_data(
        df2, units2, x_col2, y_col2,
        x_min=x_min2, x_max=x_max2, y_min=y_min2, y_max=y_max2,
        x_step=x_step2, y_step=y_step2, n_plots=2
    )

    return render_template('subplots.html',
                           files=excel_file_names,
                           selected_file1=selected_file1, x_col1=x_col1, y_col1=y_col1,
                           x_min1=x_min1, x_max1=x_max1, y_min1=y_min1, y_max1=y_max1,
                           x_step1=x_step1, y_step1=y_step1, plot_html1=plot_url1,
                           selected_file2=selected_file2, x_col2=x_col2, y_col2=y_col2,
                           x_min2=x_min2, x_max2=x_max2, y_min2=y_min2, y_max2=y_max2,
                           x_step2=x_step2, y_step2=y_step2, plot_html2=plot_url2,
                           columns1=df1.columns, columns2=df2.columns)


# Route für den PDF-Download
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    pdf_bytes = io.BytesIO()  # Erstelle ein BytesIO-Objekt für den PDF-Export

    # Eingaben für die erste Spur
    selected_file1 = request.form.get('file1')
    x_col1 = request.form.get('x_col1')
    y_col1 = request.form.get('y_col1')

    # Eingaben für die zweite Spur (falls vorhanden)
    selected_file2 = request.form.get('file2')
    x_col2 = request.form.get('x_col2')
    y_col2 = request.form.get('y_col2')

    # Eingaben für die dritte Spur (falls vorhanden)
    selected_file3 = request.form.get('file3')
    x_col3 = request.form.get('x_col3')
    y_col3 = request.form.get('y_col3')

    # Eingaben für Achsengrenzen und Schrittweiten
    x_min = request.form.get('x_min')
    x_max = request.form.get('x_max')
    y_min = request.form.get('y_min')
    y_max = request.form.get('y_max')
    x_step = request.form.get('x_step')
    y_step = request.form.get('y_step')

    # Konvertiere die Werte in floats, wenn sie vorhanden sind
    x_min = float(x_min) if x_min else None
    x_max = float(x_max) if x_max else None
    y_min = float(y_min) if y_min else None
    y_max = float(y_max) if y_max else None
    x_step = float(x_step) if x_step else None
    y_step = float(y_step) if y_step else None

    # Verarbeite den ersten Datensatz
    processed_file_path1 = os.path.join("Processed_data", f'processed_{selected_file1}.pkl')
    try:
        df1 = pd.read_pickle(processed_file_path1)
    except FileNotFoundError:
        df1 = datasets[selected_file1]
    units = units_data[selected_file1]

    # Verarbeite den zweiten Datensatz (falls ausgewählt)
    if selected_file2:
        processed_file_path2 = os.path.join("Processed_data", f'processed_{selected_file2}.pkl')
        try:
            df2 = pd.read_pickle(processed_file_path2)
        except FileNotFoundError:
            df2 = datasets[selected_file2]
    else:
        df2 = None

    # Verarbeite den dritten Datensatz (falls ausgewählt)
    if selected_file3:
        processed_file_path3 = os.path.join("Processed_data", f'processed_{selected_file3}.pkl')
        try:
            df3 = pd.read_pickle(processed_file_path3)
        except FileNotFoundError:
            df3 = datasets[selected_file3]
    else:
        df3 = None

    # Erstelle den Plot als PDF mit Achsengrenzen und Schrittweiten
    pdf_bytes = plot_data_with_traces(
        df1, units, x_col1, y_col1,
        df2, x_col2, y_col2,
        df3, x_col3, y_col3,
        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
        x_step=x_step, y_step=y_step,
        output_format='pdf'
    )

    # Erstelle den Dateinamen für das PDF basierend auf den ausgewählten Spuren
    pdf_filename = generate_pdf_filename(
        selected_file1, x_col1, y_col1,
        selected_file2, y_col2,
        selected_file3, y_col3
    )

    # Erstelle den Pfad im "PDF_Export"-Ordner
    pdf_path = os.path.join("PDF_Export", pdf_filename)

    # Speichere das PDF im Ordner "PDF_Export"
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes.getvalue())

    # Rückgabe des PDF-Inhalts direkt aus BytesIO, ohne es auf der Festplatte zu speichern
    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name=pdf_filename,
        mimetype='application/pdf'
    )


# Funktion zur Generierung des kürzeren Dateinamens für das PDF
def generate_pdf_filename(selected_file1, x_col1, y_col1, selected_file2=None, y_col2=None, selected_file3=None, y_col3=None):
    # Erstelle eine kürzere Version des Dateinamens, indem nur die ersten 5 Zeichen der Dateinamen verwendet werden
    base_filename = f"{selected_file1.split('.')[0][:5]}_{y_col1[:5]}_{x_col1[:5]}"

    # Füge Spur 2 hinzu, falls vorhanden, und kürze die Namen
    if selected_file2 and y_col2:
        base_filename += f"_{selected_file2.split('.')[0][:5]}_{y_col2[:5]}"

    # Füge Spur 3 hinzu, falls vorhanden, und kürze die Namen
    if selected_file3 and y_col3:
        base_filename += f"_{selected_file3.split('.')[0][:5]}_{y_col3[:5]}"

    # Rückgabe des gekürzten Dateinamens
    return base_filename + ".pdf"



if __name__ == '__main__':
    app.run(debug=True)
