import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt


def create_radar_chart(stats, color):
    """Crea un grafico radar per le statistiche del personaggio usando matplotlib"""
    # Categorie e valori
    categories = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    values = [stats['STR'], stats['DEX'], stats['CON'], stats['INT'], stats['WIS'], stats['CHA']]

    # Numero di variabili
    N = len(categories)

    # Crea gli angoli per ogni asse (divisi equamente)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Chiudi il cerchio

    # Aggiungi il valore iniziale anche alla fine per chiudere il poligono
    values += values[:1]

    # Crea la figura
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Disegna il grafico principale (poligono colorato)
    ax.fill(angles, values, color=color, alpha=0.25)
    ax.plot(angles, values, color=color, linewidth=3)

    # Aggiungi punti ai vertici
    ax.scatter(angles, values, s=250, color=color, alpha=0.7)

    # Imposta il limite dell'asse y a 22 (max valore possibile delle stat)
    ax.set_ylim(0, 22)

    # Etichette e valori per ogni asse
    for i, (angle, value, category) in enumerate(zip(angles[:-1], values[:-1], categories)):
        # Calcola la posizione x,y per le etichette FUORI dal grafico
        # Usa coordinate cartesiane per un miglior posizionamento
        label_dist = 25  # Distanza dal centro (oltre il raggio max di 22)
        x = label_dist * np.cos(angle)
        y = label_dist * np.sin(angle)

        # Posiziona l'etichetta della categoria fuori dal radar
        # Aggiusta l'allineamento del testo in base alla posizione
        ha = 'center'
        if abs(np.cos(angle)) > 0.7:  # Etichette a destra o sinistra
            ha = 'left' if np.cos(angle) < 0 else 'right'

        va = 'center'
        if abs(np.sin(angle)) > 0.7:  # Etichette in alto o in basso
            va = 'bottom' if np.sin(angle) > 0 else 'top'

        # Converti coordinate cartesiane a polari per il posizionamento del testo
        ax.annotate(
            category,
            xy=(angle, 22),  # Punto di ancoraggio all'estremità dell'asse
            xytext=(angle, 24),  # Testo leggermente fuori dal grafico
            fontsize=16,
            fontweight='bold',
            ha=ha,
            va=va
        )

        # Posiziona il valore della statistica accanto al punto
        ax.text(angle, value + 0.8, str(value), ha='center', va='center', size=15, weight='bold',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor=color, boxstyle='round,pad=0.4'))

    # Configura gli assi
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])  # Rimuovi le etichette predefinite

    # Rimuovi le etichette dell'asse y ma mantieni la griglia radiale
    ax.set_yticklabels([])

    # Aggiungi cerchi concentrici come riferimento
    for i in range(5, 22, 5):
        ax.text(np.pi / 2, i, str(i), ha='center', va='bottom', color='gray', fontsize=12)
        circle = plt.Circle((0, 0), i, transform=ax.transData._b, fill=False, edgecolor='gray', alpha=0.5,
                            linestyle='--')
        ax.add_artist(circle)

    # Pulisci il layout
    plt.tight_layout()

    return fig


def create_bar_chart(scores, color):
    """Crea un grafico a barre con i punteggi di tutte le classi"""
    # Prepara i dati per il grafico a barre
    data = pd.DataFrame({
        'Classe': list(scores.keys()),
        'Punteggio': list(scores.values())
    })

    # Traduci le classi in italiano
    class_translations = {
        'barbarian': 'Barbarian',
        'rogue': 'Rogue',
        'wizard': 'Wizard',
        'cleric': 'Cleric',
        'druid': 'Druid',
        'monk': 'Monk'
    }

    data['Classe_IT'] = data['Classe'].map(class_translations)

    # Calcola le percentuali
    total_questions = sum(scores.values())
    data['Percentuale'] = data['Punteggio'] / total_questions * 100

    # Crea il grafico a barre
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Percentuale:Q', title='Percentage (%)'),
        y=alt.Y('Classe_IT:N', title='Class', sort='-x'),
        color=alt.condition(alt.datum.Classe == max(scores, key=scores.get), alt.value(color), alt.value('gray')),
        tooltip=['Classe_IT', 'Punteggio', alt.Tooltip('Percentuale:Q', format='.1f')]
    ).properties(
        title='Distribution',
        width=600,
        height=300
    )

    return chart

