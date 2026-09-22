import io
import pandas as pd
import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Questionario PROVA",
    layout="centered",
)

# ==============================================================================
#  SEZIONE MODIFICABILE: PUOI MODIFICARE O AGGIUNGERE OPZIONI QUI SOTTO
# ==============================================================================

OPZIONI_AMBITI = ["Italia", "Europa"]
OPZIONI_EUROPA = ["Austria", "Belgio", "Francia", "Germania", "Spagna"]
OPZIONI_PT = ["PT1", "PT2", "PT3", "PT4", "PT14", "PT18", "PT19"]
OPZIONI_STATO_REGOLATORIO = ["Approvato", "In revisione"]
OPZIONI_BASSO_RISCHIO = ["Sì", "No"]
OPZIONI_PRODUZIONE_FISICA = ["Sì", "No"]

STATI_EUROPA = [
    "Austria", "Belgio", "Bulgaria", "Cipro", "Croazia", "Danimarca", "Estonia",
    "Finlandia", "Francia", "Germania", "Grecia", "Irlanda", "Italia", "Lettonia",
    "Lituania", "Lussemburgo", "Malta", "Paesi Bassi", "Polonia", "Portogallo",
    "Repubblica Ceca", "Romania", "Slovacchia", "Slovenia", "Spagna", "Svezia", "Ungheria"
]

REGIONI_ITALIA = [
    "Valle d'Aosta", "Piemonte", "Liguria", "Lombardia", "Trentino-Alto Adige",
    "Veneto", "Friuli-Venezia Giulia", "Emilia-Romagna", "Toscana", "Umbria",
    "Marche", "Lazio", "Abruzzo", "Molise", "Campania", "Puglia", "Basilicata",
    "Calabria", "Sicilia", "Sardegna"
]

PROVINCE_PER_REGIONE = {
    "Valle d'Aosta": ["Aosta"],
    "Piemonte": ["Alessandria", "Asti", "Biella", "Cuneo", "Novara", "Torino", "Verbano-Cusio-Ossola", "Vercelli"],
    "Liguria": ["Genova", "Imperia", "La Spezia", "Savona"],
    "Lombardia": ["Bergamo", "Brescia", "Como", "Cremona", "Lecco", "Lodi", "Mantova", "Milano", "Monza e della Brianza", "Pavia", "Sondrio", "Varese"],
    "Trentino-Alto Adige": ["Bolzano", "Trento"],
    "Veneto": ["Belluno", "Padova", "Rovigo", "Treviso", "Venezia", "Verona", "Vicenza"],
    "Friuli-Venezia Giulia": ["Gorizia", "Pordenone", "Trieste", "Udine"],
    "Emilia-Romagna": ["Bologna", "Ferrara", "Forlì-Cesena", "Modena", "Parma", "Piacenza", "Ravenna", "Reggio Emilia", "Rimini"],
    "Toscana": ["Arezzo", "Firenze", "Grosseto", "Livorno", "Lucca", "Massa-Carrara", "Pisa", "Pistoia", "Prato", "Siena"],
    "Umbria": ["Perugia", "Terni"],
    "Marche": ["Ancona", "Ascoli Piceno", "Fermo", "Macerata", "Pesaro e Urbino"],
    "Lazio": ["Frosinone", "Latina", "Rieti", "Roma", "Viterbo"],
    "Abruzzo": ["Chieti", "L'Aquila", "Pescara", "Teramo"],
    "Molise": ["Campobasso", "Isernia"],
    "Campania": ["Avellino", "Benevento", "Caserta", "Napoli", "Salerno"],
    "Puglia": ["Bari", "Barletta-Andria-Trani", "Brindisi", "Foggia", "Lecce", "Taranto"],
    "Basilicata": ["Matera", "Potenza"],
    "Calabria": ["Catanzaro", "Cosenza", "Crotone", "Reggio Calabria", "Vibo Valentia"],
    "Sicilia": ["Agrigento", "Caltanissetta", "Catania", "Enna", "Messina", "Palermo", "Ragusa", "Siracusa", "Trapani"],
    "Sardegna": ["Cagliari", "Nuoro", "Oristano", "Sassari", "Sud Sardegna"]
}

# ==============================================================================
# INIZIALIZZAZIONE STATO
# ==============================================================================
if "sostanze_list" not in st.session_state:
    st.session_state.sostanze_list = [
        {
            "nome": "",
            "cas": "",
            "ec": "",
            "pt": [],
            "stato_reg": OPZIONI_STATO_REGOLATORIO[0],
            "basso_rischio": "No",
        }
    ]

def aggiungi_sostanza():
    st.session_state.sostanze_list.append(
        {
            "nome": "",
            "cas": "",
            "ec": "",
            "pt": [],
            "stato_reg": OPZIONI_STATO_REGOLATORIO[0],
            "basso_rischio": "No",
        }
    )

def rimuovi_sostanza(index):
    if len(st.session_state.sostanze_list) > 1:
        st.session_state.sostanze_list.pop(index)

# ==============================================================================
# INTERFACCIA UTENTE
# ==============================================================================
st.title("Questionario Autorizzazioni & Sostanze Attive")
st.markdown("Compilare tutti i campi richiesti per la registrazione dei dati.")

# 1. SEDE TITOLARE
st.header("1. Sede Titolare Autorizzazione")
ambiti = st.multiselect(
    "Seleziona ambito/i di autorizzazione:",
    options=OPZIONI_EUROPA,
    help="",
)



if "Europa" in ambiti:
    stato_eu = st.selectbox(
        "Stato Europeo Sede Titolare *",
        options=["Prego selezionare..."] + STATI_EUROPA,
    )

st.divider()

# 2. STABILIMENTO
st.header("2. Ubicazione Stabilimento")
col_sr, col_sp = st.columns(2)

with col_sr:
    regione_stab = st.selectbox(
        "Regione Stabilimento *",
        options=["Prego selezionare..."] + REGIONI_ITALIA,
    )

with col_sp:
    prov_stab_opts = PROVINCE_PER_REGIONE.get(regione_stab, []) if regione_stab != "Prego selezionare..." else []
    provincia_stab = st.selectbox(
        "Provincia Stabilimento *",
        options=["Prego selezionare..."] + prov_stab_opts,
    )

st.divider()

# 3. PRODUZIONE FISICA
st.header("3. Produzione Fisica")
prod_fisica = st.radio(
    "L'azienda effettua produzione fisica?",
    options=OPZIONI_PRODUZIONE_FISICA,
    horizontal=True,
)

st.divider()

# 4. SCHEDA SOSTANZA ATTIVA
st.header("4. Scheda Sostanza Attiva")
st.caption("Identificazione della sostanza e posizione regolatoria. Puoi aggiungere più sostanze.")

for idx, sostanza in enumerate(st.session_state.sostanze_list):
    titolo_expander = f"🧪 Sostanza #{idx + 1}: {sostanza['nome']}" if sostanza["nome"] else f"🧪 Sostanza #{idx + 1} (Da compilare)"

    with st.expander(titolo_expander, expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            sostanza["nome"] = st.text_input("Nome della sostanza *", value=sostanza["nome"], key=f"nome_{idx}")
            sostanza["cas"] = st.text_input("CAS Number", value=sostanza["cas"], key=f"cas_{idx}")
        with c2:
            sostanza["ec"] = st.text_input("EC Number", value=sostanza["ec"], key=f"ec_{idx}")
            idx_stato = OPZIONI_STATO_REGOLATORIO.index(sostanza["stato_reg"]) if sostanza["stato_reg"] in OPZIONI_STATO_REGOLATORIO else 0
            sostanza["stato_reg"] = st.selectbox("Stato regolatorio del PA *", options=OPZIONI_STATO_REGOLATORIO, index=idx_stato, key=f"stato_{idx}")

        sostanza["pt"] = st.multiselect("PT di interesse:", options=OPZIONI_PT, default=sostanza["pt"], key=f"pt_{idx}")
        idx_rischio = OPZIONI_BASSO_RISCHIO.index(sostanza["basso_rischio"]) if sostanza["basso_rischio"] in OPZIONI_BASSO_RISCHIO else 1
        sostanza["basso_rischio"] = st.radio("Basso rischio?", options=OPZIONI_BASSO_RISCHIO, index=idx_rischio, horizontal=True, key=f"rischio_{idx}")

        if len(st.session_state.sostanze_list) > 1:
            st.button(f"🗑️ Rimuovi Sostanza #{idx + 1}", on_click=rimuovi_sostanza, args=(idx,), key=f"btn_del_{idx}")

st.button("➕ Aggiungi un'altra sostanza attiva", on_click=aggiungi_sostanza, type="secondary")

st.divider()

# ==============================================================================
# INVIO ED ESPORTAZIONE
# ==============================================================================
if st.button("🚀 Invia Questionario", type="primary", use_container_width=True):
    errori = []
    if not ambiti:
        errori.append("Selezionare almeno un ambito per la Sede Titolare.")
    if "Italia" in ambiti and (regione_tit == "Prego selezionare..." or provincia_tit == "Prego selezionare..."):
        errori.append("Completare Regione e Provincia per la Sede Italia.")
    if "Europa" in ambiti and stato_eu == "Prego selezionare...":
        errori.append("Selezionare lo Stato per la Sede Europa.")
    if regione_stab == "Prego selezionare..." or provincia_stab == "Prego selezionare...":
        errori.append("Completare Regione e Provincia dello Stabilimento.")

    for i, s in enumerate(st.session_state.sostanze_list):
        if not s["nome"].strip():
            errori.append(f"Inserire il Nome per la Sostanza #{i + 1}.")

    if errori:
        for err in errori:
            st.error(f"⚠️ {err}")
    else:
        st.success("✅ Questionario inviato con successo!")
        dati_finali = []
        for s in st.session_state.sostanze_list:
            dati_finali.append({
                "Ambiti Sede": ", ".join(ambiti),
                "Regione Sede": regione_tit,
                "Provincia Sede": provincia_tit,
                "Stato Europa": stato_eu,
                "Regione Stabilimento": regione_stab,
                "Provincia Stabilimento": provincia_stab,
                "Produzione Fisica": prod_fisica,
                "Nome Sostanza": s["nome"],
                "CAS Number": s["cas"] or "N/A",
                "EC Number": s["ec"] or "N/A",
                "PT Interesse": ", ".join(s["pt"]) if s["pt"] else "Nessuno",
                "Stato Regolatorio PA": s["stato_reg"],
                "Basso Rischio": s["basso_rischio"],
            })

        df = pd.DataFrame(dati_finali)
        st.subheader("📊 Tabella Risposte")
        st.dataframe(df, use_container_width=True)

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button("📥 Scarica CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="risposte.csv", mime="text/csv", use_container_width=True)
        with col_dl2:
            buffer_excel = io.BytesIO()
            with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Risposte")
            st.download_button("📊 Scarica Excel (.xlsx)", data=buffer_excel.getvalue(), file_name="risposte.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
