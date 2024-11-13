def data_processing(df, units):
    """
    Bearbeitet und erweitert einen Datensatz, indem neue Spalten für bestimmte Berechnungen hinzugefügt werden
    und die Einheiten entsprechend im DataFrame `units` aktualisiert werden.

    :param df: DataFrame, der die Daten aus einer Excel-Datei enthält
    :param units: DataFrame, der die Einheiten der Spalten im DataFrame speichert
    :return: Aktualisierter DataFrame und der aktualisierte Einheiten-DataFrame
    """

    # Benutzerdefinierte Berechnungen: Berechnung der Mittelwerte für Nord- und Südrichtung
    # Die Mittelwerte werden für jeweils zwei Spalten berechnet, um Verdrehungen zu bestimmen.
    df['u_m_N_sup'] = df[['u_10', 'u_11']].mean(axis=1)
    df['u_m_N_inf'] = df[['u_12', 'u_13']].mean(axis=1)
    df['u_m_S_sup'] = df[['u_14', 'u_15']].mean(axis=1)
    df['u_m_S_inf'] = df[['u_16', 'u_17']].mean(axis=1)

    # Einheitenzuweisung für die neu berechneten Spalten
    units.loc['u_m_N_sup'] = 'mm'
    units.loc['u_m_N_inf'] = 'mm'
    units.loc['u_m_S_sup'] = 'mm'
    units.loc['u_m_S_inf'] = 'mm'

    # Berechnung der relativen Verdrehung in Nord- und Südrichtung in Milliradiant (mrad)
    df['psi_rel_N'] = (df['u_m_N_inf'] - df['u_m_N_sup']) / 630 * 1000
    df['psi_rel_S'] = (df['u_m_S_inf'] - df['u_m_S_sup']) / 630 * 1000

    # Einheitenzuweisung für die Spalten 'psi_rel_N' und 'psi_rel_S'
    units.loc['psi_rel_N'] = 'mrad'
    units.loc['psi_rel_S'] = 'mrad'

    # Berechnung der Differenz zwischen den Werten in den Spalten 'w_sup' und 'w_inf'
    df['w_delta'] = -df['w_sup'] + df['w_inf']

    # Berechnung des Mittelwerts der Spalten 'w_03' und 'w_04'
    df['u_m'] = 0.5 * (df['w_03'] + df['w_04'])

    # Berechnung des absoluten Werts der Spalte 'KMD_2MN'
    df['Q_sup'] = df['KMD_2MN'].abs()

    # Berechnung einer Größe basierend auf 'oeldruck_P8AP' und Skalierung
    df['Q_oel'] = df['oeldruck_P8AP'].abs() / 10 * 36570 / 1000

    # Berechnung der Mittelwerte für Nord- und Südrichtung basierend auf den Spalten 'w_01' und 'w_02' sowie 'w_03' und 'w_04'
    df['w_m_N'] = df[['w_01', 'w_02']].mean(axis=1)
    df['w_m_S'] = df[['w_03', 'w_04']].mean(axis=1)

    # Einheitenzuweisung für die Mittelwertspalten
    units.loc['w_m_N'] = 'mm'
    units.loc['w_m_S'] = 'mm'

    """
    Ab hier können neue Spalten ergänzt werden, aber es ist wichtig, dass für jede neue Spalte auch eine 
    entsprechende Einheit im `units`-DataFrame hinzugefügt wird. 

    Beispiel für das Hinzufügen einer neuen Spalte:
    df['neue_spalte'] = <Berechnung>
    units.loc['neue_spalte'] = '<Einheit>'

    Dadurch wird sichergestellt, dass alle Daten korrekt skaliert und dokumentiert sind.
    """

    # Sortiere die Spaltennamen alphabetisch unter Beachtung der Groß- und Kleinschreibung
    df = df.reindex(sorted(df.columns, key=lambda x: x.lower()), axis=1)

    # Rückgabe des bearbeiteten DataFrames und des aktualisierten Einheiten-DataFrames
    return df, units
