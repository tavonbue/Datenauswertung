# Funktion, um zu überprüfen, ob eine Zelle numerisch ist
def is_numeric(val):
    import pandas as pd
    try:
        pd.to_numeric(val)
        return True
    except ValueError:
        return False

def plot_function(df, x_columns, y, title, x_label, y_label):
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('TkAgg')

    # Erstellen einer neuen Figur und Achsen
    plt.figure(figsize=(15, 8), dpi=100)

    # Schleife über alle Verformungsspalten und die entsprechenden Kurven plotten
    for col in x_columns:
        # Plotten der Verformung auf der X-Achse und der Kraft Q_sup auf der Y-Achse
        plt.plot(df[col].clip(lower=0), y, label=f'{col} vs. {y.name}')

    # Titel und Achsenbeschriftungen
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Legende anzeigen
    plt.legend()

    # Diagramm anzeigen
    plt.grid(True)
    plt.show()