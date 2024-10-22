def plot_data(df, units, x_col, y_col):
    # Plot-Funktion für flexible Achsen
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    import matplotlib

    matplotlib.use('Agg')  # Setzt das nicht-interaktive Backend für das Plotten
    plt.figure(figsize=(10, 7))
    plt.plot(df[x_col], df[y_col], label=f'{x_col} vs. {y_col}', color='blue')
    plt.title(f'{x_col} vs. {y_col}')
    plt.xlabel(f'{x_col} [{units.loc[x_col]}]')
    plt.ylabel(f'{y_col} [{units.loc[y_col]}]')
    plt.grid(True)

    # Bild in Bytes konvertieren und Base64 kodieren
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url