import os
import yaml
import streamlit as st
from pathlib import Path
from plots import create_radar_chart, create_bar_chart


def load_yaml_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


# Configurazione pagina
st.set_page_config(
    page_title="D&P Test",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
    /* Nascondi menu principale */
    #MainMenu {visibility: hidden !important;}

    /* Nascondi footer */
    footer {visibility: hidden !important;}

    /* Nascondi header e altri elementi di Streamlit */
    header {visibility: hidden !important;}

    /* Nascondi il pulsante deploy */
    .stDeployButton {display: none !important;}

    /* Nascondi la barra degli strumenti */
    .stToolbar {display: none !important;}

    /* Nascondi decorazioni Streamlit */
    .stDecoration {display: none !important;}

    /* Nascondi elementi di Streamlit Community Cloud */
    .viewerBadge_container__1QSob {display: none !important;}
    .viewerBadge_link__1S137 {display: none !important;}
    .stApp a:first-child {display: none !important;}
    .styles_viewerBadge__CvC9N {display: none !important;}

    /* Nascondi altri possibili elementi */
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Stili CSS personalizzati
st.markdown("""
<style>
    body {
        font-size: 14px;
    }
    .main-title {
        font-size: 2.6rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1.3rem;
        color: #306998;
    }
    .class-title {
        font-size: 2rem !important;
        font-weight: bold;
        color: #306998;
        margin-top: 1.3rem;
    }
    .stats-box {
        background-color: #f0f2f6;
        padding: 1.3rem;
        border-radius: 0.7rem;
        margin: 1.3rem 0;
    }
    .special-move {
        padding: 0.7rem;
        background-color: #ffd43b;
        margin: 0.7rem 0;
        border-radius: 0.4rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .description-text {
        font-size: 1.2rem !important;
        line-height: 1.6;
        margin: 1.3rem 0;
    }
    .python-zen {
        font-style: italic;
        text-align: center;
        padding: 1.3rem;
        background-color: #306998;
        color: white;
        border-radius: 0.6rem;
        margin: 1.3rem 0;
        font-size: 1.1rem;
    }
    .stButton button {
        font-size: 1.1rem;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
    }
    h1, h2, h3 {
        font-size: 1.6rem !important;
    }
    .stRadio label {
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)


class PythonDevTest:
    def __init__(self):
        self.scores = {
            "barbarian": 0,
            "rogue": 0,
            "wizard": 0,
            "cleric": 0,
            "druid": 0,
            "monk": 0
        }

        self.questions = load_yaml_file("copy/questions.yaml")

        # Dictionary comprehension con pathlib
        character_dir = Path("copy/character")
        self.results = {path.stem: load_yaml_file(path) for path in character_dir.glob("*.yaml")}

    def reset_scores(self):
        """Reimposta tutti i punteggi a zero"""
        for class_name in self.scores:
            self.scores[class_name] = 0


def intro_page():
    """Mostra la pagina introduttiva del test"""
    st.markdown('<div class="main-title">🐍 Dungeons & Pythons 🐍</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="description-text">
    Welcome, <b>adventurer</b> of Python code!
    
    This test will analyze your skills and preferences to determine
    which class of Python developer best matches your style.
    
    Are you a <b>Barbarian</b> who solves problems with brute force?<br>
    A <b>Rogue</b> who “borrows” code from others?<br>
    A <b>Wizard</b> who masters the arcane arts of metaclasses?<br>
    A <b>Cleric</b> devoted to testing and best practices?<br>
    A <b>Druid</b> in harmony with hardware and data?<br>
    Or a <b>Monk</b> who has attained the enlightenment of simplicity?
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start the Test", use_container_width=True):
            st.session_state.page = "questions"
            st.session_state.question_index = 0
            st.rerun()


def question_page(test):
    """Mostra la pagina con le domande del test"""
    question_index = st.session_state.question_index
    total_questions = len(test.questions)

    # Mostra la barra di progresso
    progress = question_index / total_questions
    st.progress(progress)
    st.markdown(f"<h3 style='text-align: center;'>Question {question_index + 1} of {total_questions}</h3>",
                unsafe_allow_html=True)

    # Mostra la domanda corrente
    question = test.questions[question_index]
    st.markdown(f"### {question['text']}", unsafe_allow_html=True)

    # Crea una lista di opzioni per il radio button
    options = [opt[0] for opt in question['options']]

    # Mostra le opzioni come radio button con stile personalizzato
    st.markdown("""
    <style>
    div.row-widget.stRadio > div {
        flex-direction: column;
        gap: 8px;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        padding: 12px;
        background-color: #f0f2f6;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: #e6e9ef;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label > div:first-child {
        transform: scale(1.2);
    }
    </style>
    """, unsafe_allow_html=True)

    choice = st.radio("Choose the option that best represents you:", options, index=None, key=f"q_{question_index}")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Mostra pulsante per continuare solo se è stata selezionata un'opzione
        if choice is not None:
            choice_index = options.index(choice)
            selected_class = question['options'][choice_index][1]

            if st.button("Continue", use_container_width=True, key="continua_btn", help="Next question"):
                # Aggiorna il punteggio
                test.scores[selected_class] += 1

                # Passa alla prossima domanda o ai risultati
                if question_index < total_questions - 1:
                    st.session_state.question_index += 1
                else:
                    st.session_state.page = "results"

                st.rerun()


def results_page(test):
    """Mostra la pagina dei risultati del test"""
    # Determina la classe con il punteggio più alto
    # Inizializza variabili
    max_score = 0
    result_class = None
    max_count = 0
    classes_with_max = []

    # Trova il punteggio massimo
    for class_name, score in test.scores.items():
        if score > max_score:
            max_score = score

    # Conta quante classi hanno questo punteggio massimo
    for class_name, score in test.scores.items():
        if score == max_score:
            classes_with_max.append(class_name)

    # Determina il risultato in base al conteggio
    if len(classes_with_max) > 1:
        # Se due classi hanno lo stesso punteggio, scegli casualmente
        result_class = "master"
    else:
        # Se una sola classe ha il punteggio massimo
        result_class = classes_with_max[0]

    result = test.results[result_class]

    # Mostra l'intestazione con il risultato
    st.markdown(f'<div class="main-title">Your result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="class-title">{result["title"]}</div>', unsafe_allow_html=True)

    # Layout per immagine e descrizione
    col1, col2 = st.columns([1, 2])

    with col1:
        # Mostra l'immagine del personaggio
        try:
            # Ottieni il percorso assoluto della directory corrente
            current_dir = Path(__file__).parent.absolute()
            image_path = os.path.join(current_dir, result["image"])

            # Carica l'immagine se esiste
            if os.path.exists(image_path):
                st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
                st.image(image_path, use_container_width=True)
            else:
                # Gestisci silenziosamente il caso in cui l'immagine non esiste
                st.markdown("⚠️ *Character image not available*")
        except Exception:
            # Ignora l'errore e continua senza l'immagine
            pass

    with col2:
        # Mostra la descrizione
        st.markdown(f'<div class="description-text">{result["description"]}</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([2, 3])

    if result_class != "master":
        with col3:
            # Mostra le statistiche come grafico radar
            st.subheader("Statistics")
            radar_chart = create_radar_chart(result["stats"], result["color"])
            st.pyplot(radar_chart)

        with col4:
            # Mostra il grafico a barre con tutti i punteggi
            bar_chart = create_bar_chart(test.scores, result["color"])
            st.altair_chart(bar_chart, use_container_width=True)

    # Mostra un messaggio di saggezza personalizzato in base alla classe
    st.markdown("""
        <style>
        .python-zen {
            background-color: #f8f8f8;
            border-left: 6px solid #4B8BBE;
            padding: 1em;
            font-family: 'Courier New', monospace;
            font-size: 15px;
            white-space: pre-line;
            line-height: 1.6;
            border-radius: 5px;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div class="python-zen">{result["message"]}</div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Retry", use_container_width=True):
            # Resetta i punteggi
            test.reset_scores()
            st.session_state.page = "intro"
            st.rerun()

    # Aggiungi un easter egg in base alla classe risultante
    if "easter_egg" in result.keys():
        if st.button(result["easter_egg"]["name_button"]):
            st.code(result["easter_egg"]["text"], language="python")


def main():
    # Inizializza la sessione
    if 'page' not in st.session_state:
        st.session_state.page = "intro"

    if 'test' not in st.session_state:
        st.session_state.test = PythonDevTest()

    # Gestisci le pagine
    if st.session_state.page == "intro":
        intro_page()
    elif st.session_state.page == "questions":
        question_page(st.session_state.test)
    elif st.session_state.page == "results":
        results_page(st.session_state.test)


if __name__ == "__main__":
    main()
