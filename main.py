import pandas as pd
from functions import is_numeric, plot_function

# Pfad zur Datei
file_path = '../02_ST01_01/hilti_timbertesting_ST01_01_messdaten.xlsx'

# Excel-Datei einlesen, erste Zeile überspringen, erste Spalte als Index festlegen und leere Zeilen entfernen
df_raw = pd.read_excel(file_path, skiprows=1, index_col=0).dropna(how='all', axis=0)

# Die map-Methode auf jede Spalte anwenden und nur Zeilen behalten, die numerische Werte enthalten
df = df_raw[df_raw.apply(lambda row: row.map(is_numeric).all(), axis=1)]

# Einheiten auslesen
cleaned_units = df_raw.iloc[0, :].str.strip()

# Anpassungen am Datensatz
df.loc[:, 'w_delta'] = -df['w_sup']+df['w_inf']
df.loc[:, 'u_m'] = 0.5*(df['w_03']+df['w_04'])
df.loc[:, 'Q_sup'] = df['KMD_2MN'].abs()
df.loc[:, 'Q_oel'] = df['oeldruck_P8AP'].abs()/10*36570/1000
df.loc[:, 'psi_rel_N'] = (0.5*(df['u_10']+df['u_11'])-0.5*(df['u_12']+df['u_13']))/630
df.loc[:, 'psi_rel_S'] = (0.5*(df['u_14']+df['u_15'])-0.5*(df['u_16']+df['u_17']))/630
print(df)

# Liste der Verformungsspalten
w_cols = ['w_01', 'w_02', 'w_03', 'w_04', 'w_sup', 'w_inf']
u_cols = ['u_01', 'u_02', 'u_03', 'u_04', 'u_10', 'u_11', 'u_12', 'u_13', 'u_14', 'u_15', 'u_16', 'u_17']
print(plot_function(df, w_cols, df['Q_sup'], 'Kraft-Verformungs-Diagramm', 'Verformung [mm]', 'Kraft [kN]'))
print(plot_function(df, u_cols, df['Q_sup'], 'Kraft-Verformungs-Diagramm', 'Verformung [mm]', 'Kraft [kN]'))
print(plot_function(df, ['w_delta'], df['Q_sup'], 'Kraft-Verformungs-Diagramm', 'Verformung [mm]', 'Kraft [kN]'))
print(plot_function(df, [ 'w_03', 'w_04', 'u_m'], df['Q_sup'], 'Kraft-Verformungs-Diagramm', 'Verformung [mm]', 'Kraft [kN]'))
