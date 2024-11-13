import base64
import pandas as pd
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from io import BytesIO


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
              n_plots=1, output_format='png'):

    matplotlib.use('Agg')  # Setzt das nicht-interaktive Backend für das Plotten

    # Abmessungen im Verhältnis 1:1.618
    golden_ratio = (1 + 5**0.5) / 2
    if n_plots == 1:
        width_mm = 200
        exchange = 3.937 / 100
        width_inch = width_mm * exchange
        plt.figure(figsize=(width_inch, width_inch / golden_ratio))
    else:
        width_mm = 150
        exchange = 3.937 / 100
        width_inch = width_mm * exchange
        plt.figure(figsize=(width_inch, width_inch))

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


def plotly_interactive_plot(df, units, x_col, y_col, x_min=None, x_max=None, y_min=None, y_max=None,
                            x_step=None, y_step=None, selected_points=None):
    # Erstelle das Plotly-Objekt
    fig = go.Figure()

    # Linie und Marker hinzufügen
    fig.add_trace(go.Scatter(
        x=df[x_col],  # Setzt die x-Werte auf die ausgewählte Spalte
        y=df[y_col],  # Setzt die y-Werte auf die ausgewählte Spalte
        mode='lines',  # Zeigt nur Linien an
        line=dict(color='black', width=1.5),  # Legt die Linienfarbe auf Schwarz und die Linienstärke auf 1.5 fest
        marker=dict(size=4),  # Legt die Größe der Marker fest
        name=f'{x_col} vs. {y_col}',  # Legt den Namen der Linie fest (wird aber nicht angezeigt)
        showlegend=False  # Deaktiviert die Anzeige der Legende
    ))

    # Markierte Punkte hinzufügen
    if selected_points:
        fig.add_trace(go.Scatter(
            x=[point['x'] for point in selected_points],
            y=[point['y'] for point in selected_points],
            mode='markers',
            marker=dict(size=8, color='red'),  # Markierte Punkte in Rot
            name='Selected Points',
            showlegend=False  # Deaktiviert die Anzeige der Legende für markierte Punkte
        ))

    # Achsenlabels mit Einheiten
    fig.update_layout(
        xaxis_title=f"{x_col} [{units.get(x_col, '')}]",
        yaxis_title=f"{y_col} [{units.get(y_col, '')}]",
        font=dict(family="Computer Modern, serif", size=14),
        margin=dict(l=50, r=50, t=50, b=50),
        template="plotly_white",
        hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Füge horizontale und vertikale Linie bei x=0 und y=0 hinzu
    fig.add_shape(type="line", x0=0, x1=0, y0=df[y_col].min(), y1=df[y_col].max(),
                  line=dict(color="black", width=0.7), layer="below")
    fig.add_shape(type="line", y0=0, y1=0, x0=df[x_col].min(), x1=df[x_col].max(),
                  line=dict(color="black", width=0.7), layer="below")

    # Festlegung der Achsengrenzen, falls angegeben
    if x_min is not None and x_max is not None:
        fig.update_xaxes(range=[x_min, x_max])
    if y_min is not None and y_max is not None:
        fig.update_yaxes(range=[y_min, y_max])

    # Schrittweite und Teilstriche
    if x_step:
        fig.update_xaxes(dtick=x_step, tick0=x_min)
    if y_step:
        fig.update_yaxes(dtick=y_step, tick0=y_min)

    # Zusätzliche Minor Ticks zwischen den Major Ticks
    fig.update_xaxes(showgrid=True, minor=dict(ticks="inside", showgrid=True))
    fig.update_yaxes(showgrid=True, minor=dict(ticks="inside", showgrid=True))

    # Rückgabe als HTML
    return fig.to_html(full_html=False)


def plot_data_with_subplots(df1, units1, x_col1, y_col1, df2, units2, x_col2, y_col2, x_min1=None, x_max1=None, y_min1=None, y_max1=None,
                            x_step1=None, y_step1=None,
                            x_min2=None, x_max2=None, y_min2=None, y_max2=None,
                            x_step2=None, y_step2=None, output_format='png'):

    # matplotlib.use('Agg')  # Setzt das nicht-interaktive Backend für das Plotten

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Erster Plot
    ax1.plot(df1[x_col1], df1[y_col1], label=f'{x_col1} vs. {y_col1}', color='black', linewidth=1)
    ax1.set_xlabel(f'{x_col1} [{units1.get(x_col1, "")}]', loc='right', labelpad=5)
    ax1.set_ylabel(f'{y_col1} [{units1.get(y_col1, "")}]', rotation=0, labelpad=-55, y=1.03, ha='right')
    ax1.axhline(0, color='black', linestyle='-', linewidth=0.7)
    ax1.axvline(0, color='black', linestyle='-', linewidth=0.7)

    if x_min1 is not None or x_max1 is not None:
        ax1.set_xlim(left=x_min1, right=x_max1)
    if y_min1 is not None or y_max1 is not None:
        ax1.set_ylim(bottom=y_min1, top=y_max1)

    if x_step1:
        ax1.xaxis.set_major_locator(MultipleLocator(x_step1))
    if y_step1:
        ax1.yaxis.set_major_locator(MultipleLocator(y_step1))
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))

    # Zweiter Plot
    ax2.plot(df2[x_col2], df2[y_col2], label=f'{x_col2} vs. {y_col2}', color='black', linewidth=1)
    ax2.set_xlabel(f'{x_col2} [{units2.get(x_col2, "")}]', loc='right', labelpad=5)
    ax2.set_ylabel(f'{y_col2} [{units2.get(y_col2, "")}]', rotation=0, labelpad=-55, y=1.03, ha='right')
    ax2.axhline(0, color='black', linestyle='-', linewidth=0.7)
    ax2.axvline(0, color='black', linestyle='-', linewidth=0.7)

    if x_min2 is not None or x_max2 is not None:
        ax2.set_xlim(left=x_min2, right=x_max2)
    if y_min2 is not None or y_max2 is not None:
        ax2.set_ylim(bottom=y_min2, top=y_max2)

    if x_step2:
        ax2.xaxis.set_major_locator(MultipleLocator(x_step2))
    if y_step2:
        ax2.yaxis.set_major_locator(MultipleLocator(y_step2))
    ax2.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax2.yaxis.set_minor_locator(AutoMinorLocator(2))

    fig.tight_layout()
    plt.show()

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

def plot_data_with_traces(df1, units, x_col1, y_col1, df2, x_col2, y_col2, df3, x_col3, y_col3,
                          x_min=None, x_max=None, y_min=None, y_max=None,
                          x_step=None, y_step=None, output_format='png'):
    matplotlib.use('Agg')  # Setzt das nicht-interaktive Backend für das Plotten

    # Abmessungen im Verhältnis 1:1.618
    golden_ratio = (1 + 5 ** 0.5) / 2
    width_mm = 200
    exchange = 3.937 / 100
    width_inch = width_mm * exchange
    fig, ax = plt.subplots(figsize=(width_inch, width_inch / golden_ratio))

    # Plot Spur 1
    ax.plot(df1[x_col1], df1[y_col1], label=f'{y_col1}', linewidth=1, color='black')

    # Plot Spur 2 (nur, wenn df2 und die Spaltennamen nicht None sind)
    if df2 is not None and x_col2 in df2.columns and y_col2 in df2.columns:
        ax.plot(df2[x_col2], df2[y_col2], label=f'{y_col2}', linewidth=1, color='black', linestyle='dashed')

    # Plot Spur 3 (nur, wenn df3 und die Spaltennamen nicht None sind)
    if df3 is not None and x_col3 in df3.columns and y_col3 in df3.columns:
        ax.plot(df3[x_col3], df3[y_col3], label=f'{y_col3}', linewidth=1, color='black', linestyle='dotted')

    # Achsenbeschriftungen
    ax.set_xlabel(f'{x_col1} [{units.get(x_col1, "")}]', loc='right', labelpad=5)
    ax.set_ylabel(f'{y_col1} [{units.get(y_col1, "")}]', rotation=0, labelpad=-55, y=1.03, ha='right')

    # Horizontale und vertikale Linie bei y=0 und x=0
    ax.axhline(0, color='black', linestyle='-', linewidth=0.7)
    ax.axvline(0, color='black', linestyle='-', linewidth=0.7)

    # Setze die Achsengrenzen nur, wenn Werte eingegeben wurden
    if x_min is not None or x_max is not None:
        ax.set_xlim(left=x_min, right=x_max)
    if y_min is not None or y_max is not None:
        ax.set_ylim(bottom=y_min, top=y_max)

    # Major Ticks und Minor Ticks an allen vier Seiten anzeigen
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', direction='in', length=7, width=0.7,
                   top=True, bottom=True, left=True, right=True)
    ax.tick_params(axis='both', which='minor', direction='in', length=4, width=0.7,
                   top=True, bottom=True, left=True, right=True)

    # Major und Minor Ticks konfigurieren
    if x_step:
        ax.xaxis.set_major_locator(MultipleLocator(x_step))
    if y_step:
        ax.yaxis.set_major_locator(MultipleLocator(y_step))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    # Legende unterhalb des Plots
    ax.legend(loc='upper right', bbox_to_anchor=(0.6, -0.032), frameon=False, ncol=3)
    # fig.tight_layout()

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



