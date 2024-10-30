import matplotlib.pyplot as plt
import matplotlib
import mplcursors
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from io import BytesIO
import base64

# LaTeX und Computer Modern-Schrift aktivieren
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

def plot_data(df, units, x_col, y_col, x_min=None, x_max=None, y_min=None, y_max=None, x_step=None, y_step=None,
              output_format='png'):

    matplotlib.use('Agg')  # Setzt das nicht-interaktive Backend für das Plotten

    # Abmessungen im Verhältnis 1:1.618
    width_mm = 200
    exchange = 3.937 / 100
    width_inch = width_mm * exchange
    golden_ratio = (1 + 5**0.5) / 2
    plt.figure(figsize=(width_inch, width_inch / golden_ratio))

    # Plot erstellen
    plt.plot(df[x_col], df[y_col], label=f'{x_col} vs. {y_col}', color='black', linewidth=1)
    plt.xlabel(f'{x_col} [{units.loc[x_col]}]', loc='right', labelpad=5)
    plt.ylabel(f'{y_col} [{units.loc[y_col]}]', rotation=0, labelpad=-55, y=1.03, ha='right')

    # Horizontale und vertikale Linie bei y=0 und x=0
    plt.axhline(0, color='black', linestyle='-', linewidth=0.7)
    plt.axvline(0, color='black', linestyle='-', linewidth=0.7)

    # Setze die Achsengrenzen nur, wenn Werte eingegeben wurden
    if x_min is not None or x_max is not None:
        plt.xlim(left=x_min, right=x_max)
    if y_min is not None or y_max is not None:
        plt.ylim(bottom=y_min, top=y_max)

    # Major Ticks und Minor Ticks an allen vier Seiten anzeigen
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', direction='in', length=7, width=0.7,
                    top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='both', which='minor', direction='in', length=4, width=0.7,
                    top=True, bottom=True, left=True, right=True)

    # Major und Minor Ticks konfigurieren
    if x_step:
        plt.gca().xaxis.set_major_locator(MultipleLocator(x_step))
    if y_step:
        plt.gca().yaxis.set_major_locator(MultipleLocator(y_step))
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))

    # Ausgabe je nach Format
    img = BytesIO()
    if output_format == 'pdf':
        plt.savefig(img, format='pdf')
        img.seek(0)
        plt.close()
        return img
    else:
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()
        return plot_url
