

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

    for folder in folders:
        folder_path = os.path.join(parent_directory, folder)

        # Suche nach einer Excel-Datei im aktuellen Ordner
        for file in os.listdir(folder_path):
            if file.endswith('.xlsx') or file.endswith('.XLSX'):
                file_path = os.path.join(folder_path, file)
                excel_file_paths.append(file_path)

    return excel_file_paths, folders

def load_data(file_path):
    import pandas as pd

    # Excel-Datei einlesen, erste Zeile überspringen, erste Spalte als Index festlegen und leere Zeilen entfernen
    # df_raw = pd.read_excel(file_path, skiprows=1, index_col=0).dropna(how='all', axis=0)
    df_raw = pd.read_excel(file_path, skiprows=1).dropna(how='all', axis=0)

    # Die map-Methode auf jede Spalte anwenden und nur Zeilen behalten, die numerische Werte enthalten
    df = df_raw[df_raw.apply(lambda row: row.map(is_numeric).all(), axis=1)]

    # Einheiten auslesen
    units = df_raw.iloc[0, :].str.strip()

    # Anpassungen am Datensatz
    df.loc[:, 'w_delta'] = -df['w_sup'] + df['w_inf']
    df.loc[:, 'u_m'] = 0.5 * (df['w_03'] + df['w_04'])
    df.loc[:, 'Q_sup'] = df['KMD_2MN'].abs()
    df.loc[:, 'Q_oel'] = df['oeldruck_P8AP'].abs() / 10 * 36570 / 1000
    df.loc[:, 'psi_rel_N'] = (0.5 * (df['u_10'] + df['u_11']) - 0.5 * (df['u_12'] + df['u_13'])) / 630
    df.loc[:, 'psi_rel_S'] = (0.5 * (df['u_14'] + df['u_15']) - 0.5 * (df['u_16'] + df['u_17'])) / 630

    return df, units

def is_numeric(val):
    # Funktion, um zu überprüfen, ob eine Zelle numerisch ist
    import pandas as pd
    try:
        pd.to_numeric(val)
        return True
    except ValueError:
        return False