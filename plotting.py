import matplotlib.pyplot as plt
import matplotlib
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
    plt.xlabel(f'{x_col} [{units.get(x_col, "")}]', loc='right', labelpad=5)
    plt.ylabel(f'{y_col} [{units.get(y_col, "")}]', rotation=0, labelpad=-55, y=1.03, ha='right')

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


import plotly.graph_objs as go


def plotly_interactive_plot(df, units, x_col, y_col, x_min=None, x_max=None, y_min=None, y_max=None, x_step=None,
                            y_step=None, selected_points=None):

    # Erstelle das Plotly-Objekt
    fig = go.Figure()

    # Linie und Marker hinzufügen
    fig.add_trace(go.Scatter(
        x=df[x_col],  # Setzt die x-Werte auf die ausgewählte Spalte
        y=df[y_col],  # Setzt die y-Werte auf die ausgewählte Spalte
        mode='lines',  # Zeigt eine Linie mit Markern (Punkte) an 'lines+markers', 'lines'
        line=dict(color='black', width=1.5),  # Legt die Linienfarbe auf Schwarz und die Linienstärke auf 1 fest
        marker=dict(size=4),  # Legt die Größe der Marker fest (hier auf 6 gesetzt)
        name=f'{x_col} vs. {y_col}'  # Legt den Namen der Linie für die Legende fest
    ))

    # Markierte Punkte hinzufügen
    if selected_points:
        fig.add_trace(go.Scatter(
            x=[point['x'] for point in selected_points],
            y=[point['y'] for point in selected_points],
            mode='markers',
            marker=dict(size=8, color='red'),  # Markierte Punkte in Rot
            name='Selected Points'
        ))

    # Achsenlabels mit Einheiten wie in plot_data
    fig.update_layout(
        xaxis_title=f"{x_col} [{units.get(x_col, '')}]",  # Setzt den Titel der x-Achse mit Einheit aus dem 'units'-Dictionary
        yaxis_title=f"{y_col} [{units.get(y_col, '')}]",  # Setzt den Titel der y-Achse mit Einheit aus dem 'units'-Dictionary
        font=dict(family="Computer Modern, serif", size=14),  # Legt die Schriftart und -größe fest
        # title=dict(text=f'{x_col} vs. {y_col}', x=0.5),  # Setzt den Titel des Plots und zentriert ihn horizontal
        margin=dict(l=50, r=50, t=50, b=50),  # Legt die Abstände zu den Rändern (links, rechts, oben, unten) fest
        template="plotly_white",  # Setzt das Plotly-Template auf Weiß für einen klaren Hintergrund
        hovermode="closest",  # Aktiviert interaktives Hovering bei den Datenpunkten
        plot_bgcolor="rgba(0,0,0,0)",  # Setzt den Plot-Hintergrund auf transparent (kein Hintergrund)
    )

    # Füge horizontale und vertikale Linie bei x=0 und y=0 hinzu
    fig.add_shape(type="line", x0=0, x1=0, y0=df[y_col].min(), y1=df[y_col].max(),
                  line=dict(color="black", width=0.7), layer="below")
    fig.add_shape(type="line", y0=0, y1=0, x0=df[x_col].min(), x1=df[x_col].max(),
                  line=dict(color="black", width=0.7), layer="below")

    # Festlegung der Achsengrenzen falls angegeben
    if x_min is not None and x_max is not None:
        fig.update_xaxes(range=[x_min, x_max])
    if y_min is not None and y_max is not None:
        fig.update_yaxes(range=[y_min, y_max])

    # Schrittweite und Teilstriche wie in plot_data
    if x_step:
        fig.update_xaxes(dtick=x_step, tick0=x_min)
    if y_step:
        fig.update_yaxes(dtick=y_step, tick0=y_min)

    # Zusätzliche Minor Ticks zwischen den Major Ticks
    fig.update_xaxes(showgrid=True, minor=dict(ticks="inside", showgrid=True))
    fig.update_yaxes(showgrid=True, minor=dict(ticks="inside", showgrid=True))

    # Rückgabe als HTML
    return fig.to_html(full_html=False)







