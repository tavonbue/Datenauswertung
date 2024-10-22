import pandas as pd
import matplotlib
from functions import is_numeric
matplotlib.use('TkAgg')

# Pfad zur Datei
file_path = '../02_ST01_01/hilti_timbertesting_ST01_01_messdaten.xlsx'

# Excel-Datei einlesen, erste Zeile überspringen, erste Spalte als Index festlegen und leere Zeilen entfernen
df_raw = pd.read_excel(file_path, skiprows=1, index_col=0).dropna(how='all', axis=0)

# Einheiten auslesen
units = df_raw.iloc[0, :]

# Die map-Methode auf jede Spalte anwenden und nur Zeilen behalten, die numerische Werte enthalten
df = df_raw[df_raw.apply(lambda row: row.map(is_numeric).all(), axis=1)]

# Erste Zeilen der bereinigten Datei anzeigen
print(df.head())



# Plots
df.clip(lower=0).plot(x='w_01', y='Q_sup', grid=True, title='Kraft-Verformung')
df[['u_01', 'u_02', 'u_03', 'u_04', 'u_10', 'u_11', 'u_12', 'u_13']].clip(lower=0).plot(grid=True, title='Versuchsauswertung')
df[['w_01', 'w_02', 'w_03', 'w_04', 'w_sup', 'w_inf']].clip(lower=0).plot(grid=True, title='Versuchsauswertung')



