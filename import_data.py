def load_file_paths():
    import os

    # Relativer Pfad zum übergeordneten Verzeichnis
    parent_directory = '../'  # Navigiert eine Ebene über dem aktuellen Verzeichnis

    # Name des aktuellen Ordners ermitteln
    current_folder = os.path.basename(os.getcwd())

    # Alle Ordner im übergeordneten Verzeichnis auslesen und den aktuellen Ordner ausschließen
    folders = [folder for folder in os.listdir(parent_directory) if
               os.path.isdir(os.path.join(parent_directory, folder)) and folder != current_folder]

    # Durch jeden Ordner gehen und den Pfad zur Excel-Datei generieren
    excel_file_paths = []
    excel_file_names = []

    for folder in folders:
        folder_path = os.path.join(parent_directory, folder)

        # Suche nach einer Excel-Datei im aktuellen Ordner
        for file in os.listdir(folder_path):
            if file.endswith('.xlsx') or file.endswith('.XLSX'):
                file_path = os.path.join(folder_path, file)
                excel_file_paths.append(file_path)
                excel_file_names.append(file)

    return excel_file_paths, excel_file_names, folders

def load_dataframe(file_path):
    import pandas as pd
    from datenbearbeitung import data_processing

    # Excel-Datei einlesen, erste Zeile überspringen, erste Spalte als Index festlegen und leere Zeilen entfernen
    # df_raw = pd.read_excel(file_path, skiprows=1, index_col=0).dropna(how='all', axis=0)
    df_raw = pd.read_excel(file_path, skiprows=1).dropna(how='all', axis=0)

    # Die map-Methode auf jede Spalte anwenden und nur Zeilen behalten, die numerische Werte enthalten
    df = df_raw[df_raw.apply(lambda row: row.map(is_numeric).all(), axis=1)].copy()

    # Einheiten auslesen
    units = df_raw.iloc[0, :].str.strip()

    # Import der Benutzerdefinierten Daten und überschreiben der bisheren Datensätze
    df, units = data_processing(df, units)

    return df, units

def is_numeric(val):
    # Funktion, um zu überprüfen, ob eine Zelle numerisch ist
    import pandas as pd
    try:
        pd.to_numeric(val)
        return True
    except ValueError:
        return False

def get_datasets():
    import pickle

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

    dataframes = {'Datensätze': datasets, 'Einheiten': units_data, 'Excelnamen': excel_file_paths}
    with open('dataframes.pkl', 'wb') as f:
        pickle.dump(dataframes, f)

    return datasets, units_data