import io
import pandas as pd
import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Questionario PROVA",
    layout="centered",
)

# ==============================================================================
# SEZIONE MODIFICABILE: OPZIONI E LISTE
# ==============================================================================

OPZIONI_AMBITI = ["Italia", "Europa"]
OPZIONI_PT = ["PT1", "PT2", "PT3", "PT4", "PT14", "PT18", "PT19"]
OPZIONI_STATO_REGOLATORIO = ["Approvato", "In revisione"]
OPZIONI_BASSO_RISCHIO = ["Sì", "No"]
OPZIONI_PRODUZIONE_FISICA = ["Sì", "No"]
OPZIONI_ORIGINE = ["Sintetica", "Vegetale"]

# Opzioni Prodotto
OPZIONI_TIPO_PRODOTTO = ["Biocida", "PMC (Presidio Medico Chirurgico)"]
OPZIONI_TARGET = [
    "Batteri", "Micobatteri", "Virus nudi", "Virus rivestiti",
    "Lieviti", "Spore batteriche", "Spore fungine"
]
OPZIONI_FORMULAZIONE = ["Spray", "Solido", "Liquido"]
OPZIONI_CONFEZIONAMENTO = ["< 500 ml", "Tra 500 ml e 3 L", "> 3 L"]
OPZIONI_DESTINAZIONE = ["Cute", "Superfici"]
OPZIONI_UTILIZZATORI = ["Professionali", "Non professionali"]

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
def get_empty_sostanza():
    return {
        "nome": "",
        "cas": "",
        "ec": "",
        "pt": [],
        "stato_reg": OPZIONI_STATO_REGOLATORIO[0],
        "basso_rischio": "No",
        "auth_biocida": "Sì",
        "titolare": "",
        "nome_prodotto": "",
        "officina_produzione": "",
        "fornitore_pa": "",
        "perc_attivo": "",
        "num_autorizzazione": "",
        "case_number": "",
        "stati_membro": [],
        "ruolo_stati": {},
        "origine": "Sintetica",
        "specie_botanica": "",
        "parte_pianta": "",
        "tipo_provenienza_mp": "Europa",
        "paese_provenienza_eu": "Italia",
        "paese_provenienza_extra": ""
    }

def get_empty_prodotto():
    return {
        "nome": "",
        "tipo": OPZIONI_TIPO_PRODOTTO[0],
        "target": [],
        "formulazione": OPZIONI_FORMULAZIONE[0],
        "confezionamento": OPZIONI_CONFEZIONAMENTO[0],
        "destinazione_uso": [],
        "utilizzatori": []
    }

if "sostanze_list" not in st.session_state:
    st.session_state.sostanze_list = [get_empty_sostanza(), get_empty_sostanza(), get_empty_sostanza()]

if "prodotti_list" not in st.session_state:
    st.session_state.prodotti_list = [get_empty_prodotto()]

def aggiungi_sostanza():
    st.session_state.sostanze_list.append(get_empty_sostanza())

def rimuovi_sostanza(index):
    if len(st.session_state.sostanze_list) > 1:
        st.session_state.sostanze_list.pop(index)

def aggiungi_prodotto():
    st.session_state.prodotti_list.append(get_empty_prodotto())

def rimuovi_prodotto(index):
    if len(st.session_state.prodotti_list) > 1:
        st.session_state.prodotti_list.pop(index)

# ==============================================================================
# INTERFACCIA UTENTE
# ==============================================================================
st.title("Questionario Prova")
st.markdown("Compilare tutti i campi richiesti per la registrazione dei dati.")

# 1. SEDE TITOLARE
st.header("1. Sede Titolare Autorizzazione")
ambiti_tit = st.multiselect(
    "Seleziona ambito/i di autorizzazione:",
    options=OPZIONI_AMBITI,
    key="ambiti_tit"
)

regione_tit, provincia_tit, stato_eu_tit = "N/A", "N/A", "N/A"

if "Italia" in ambiti_tit:
    col_r, col_p = st.columns(2)
    with col_r:
        regione_tit = st.selectbox(
            "Regione Sede Titolare *",
            options=["Prego selezionare..."] + REGIONI_ITALIA,
            key="regione_tit_select"
        )
    with col_p:
        prov_opts = PROVINCE_PER_REGIONE.get(regione_tit, []) if regione_tit != "Prego selezionare..." else []
        provincia_tit = st.selectbox(
            "Provincia Sede Titolare *",
            options=["Prego selezionare..."] + prov_opts,
            key="provincia_tit_select"
        )

if "Europa" in ambiti_tit:
    stato_eu_tit = st.selectbox(
        "Stato Europeo Sede Titolare *",
        options=["Prego selezionare..."] + STATI_EUROPA,
        key="stato_eu_tit_select"
    )

st.divider()

# 2. STABILIMENTO
st.header("2. Ubicazione Stabilimento")
ambiti_stab = st.multiselect(
    "Seleziona ubicazione/i stabilimento:",
    options=OPZIONI_AMBITI,
    help="Puoi selezionare sia Italia che Europa",
    key="ambiti_stab"
)

regione_stab, provincia_stab, stato_eu_stab = "N/A", "N/A", "N/A"

if "Italia" in ambiti_stab:
    col_sr, col_sp = st.columns(2)
    with col_sr:
        regione_stab = st.selectbox(
            "Regione Stabilimento *",
            options=["Prego selezionare..."] + REGIONI_ITALIA,
            key="regione_stab_select"
        )
    with col_sp:
        prov_stab_opts = PROVINCE_PER_REGIONE.get(regione_stab, []) if regione_stab != "Prego selezionare..." else []
        provincia_stab = st.selectbox(
            "Provincia Stabilimento *",
            options=["Prego selezionare..."] + prov_stab_opts,
            key="provincia_stab_select"
        )

if "Europa" in ambiti_stab:
    stato_eu_stab = st.selectbox(
        "Stato Europeo Stabilimento *",
        options=["Prego selezionare..."] + STATI_EUROPA,
        key="stato_eu_stab_select"
    )

st.divider()

# 3. PRODUZIONE FISICA
st.header("3. Produzione Fisica")
prod_fisica = st.radio(
    "L'azienda effettua produzione su territorio Italiano?",
    options=OPZIONI_PRODUZIONE_FISICA,
    horizontal=True,
)

st.divider()

# 4. SCHEDA SOSTANZA ATTIVA
st.header("4. Schede Sostanze Attive")
st.caption("Compila i dettagli per le sostanze attive presenti (minimo 1 richiesta per l'invio).")

for idx, sostanza in enumerate(st.session_state.sostanze_list):
    titolo_expander = f"Sostanza #{idx + 1}: {sostanza['nome']}" if sostanza["nome"] else f"Sostanza Attiva #{idx + 1}"

    with st.expander(titolo_expander, expanded=(idx == 0)):
        c1, c2 = st.columns(2)
        with c1:
            sostanza["nome"] = st.text_input(f"Nome Sostanza #{idx + 1}", value=sostanza["nome"], key=f"nome_{idx}")
            sostanza["cas"] = st.text_input(f"CAS Number Sostanza #{idx + 1}", value=sostanza["cas"], key=f"cas_{idx}")
        with c2:
            sostanza["ec"] = st.text_input(f"EC Number Sostanza #{idx + 1}", value=sostanza["ec"], key=f"ec_{idx}")
            idx_stato = OPZIONI_STATO_REGOLATORIO.index(sostanza["stato_reg"]) if sostanza["stato_reg"] in OPZIONI_STATO_REGOLATORIO else 0
            sostanza["stato_reg"] = st.selectbox(f"Stato regolatorio Sostanza #{idx + 1}", options=OPZIONI_STATO_REGOLATORIO, index=idx_stato, key=f"stato_{idx}")

        # --- SEZIONE: ORIGINE E MATRICE DELLA SOSTANZA ---
        st.subheader("Origine e Matrice della Sostanza")
        idx_orig = OPZIONI_ORIGINE.index(sostanza["origine"]) if sostanza["origine"] in OPZIONI_ORIGINE else 0
        sostanza["origine"] = st.radio(
            f"Origine della sostanza #{idx + 1}",
            options=OPZIONI_ORIGINE,
            index=idx_orig,
            horizontal=True,
            key=f"origine_{idx}"
        )

        if sostanza["origine"] == "Vegetale":
            col_bot1, col_bot2 = st.columns(2)
            with col_bot1:
                sostanza["specie_botanica"] = st.text_input(f"Specie botanica #{idx + 1}", value=sostanza["specie_botanica"], key=f"botanica_{idx}")
            with col_bot2:
                sostanza["parte_pianta"] = st.text_input(f"Parte della pianta utilizzata #{idx + 1}", value=sostanza["parte_pianta"], key=f"pianta_{idx}")

        st.markdown("**Paese di provenienza della materia prima**")
        sostanza["tipo_provenienza_mp"] = st.radio(
            f"Tipologia provenienza materia prima #{idx + 1}",
            options=["Europa", "Extra-UE"],
            horizontal=True,
            key=f"tipo_prov_{idx}"
        )

        if sostanza["tipo_provenienza_mp"] == "Europa":
            idx_eu = STATI_EUROPA.index(sostanza["paese_provenienza_eu"]) if sostanza["paese_provenienza_eu"] in STATI_EUROPA else 0
            sostanza["paese_provenienza_eu"] = st.selectbox(
                f"Seleziona Stato Europeo di provenienza #{idx + 1}",
                options=STATI_EUROPA,
                index=idx_eu,
                key=f"paese_eu_{idx}"
            )
        else:
            sostanza["paese_provenienza_extra"] = st.text_input(
                f"Specificare Stato Extra-UE di provenienza #{idx + 1}",
                value=sostanza["paese_provenienza_extra"],
                key=f"paese_extra_{idx}"
            )

        # --- LOGICA CONDIZIONALE STATO REGOLATORIO ---
        st.markdown("---")
        if sostanza["stato_reg"] == "In revisione":
            st.markdown(f"**Dati per la Sostanza #{idx + 1} - In revisione**")
            sostanza["titolare"] = st.text_input("Titolare", value=sostanza["titolare"], key=f"tit_rev_{idx}")
            sostanza["nome_prodotto"] = st.text_input("Nome prodotto", value=sostanza["nome_prodotto"], key=f"nprod_rev_{idx}")
            sostanza["officina_produzione"] = st.text_input("Officina produzione", value=sostanza["officina_produzione"], key=f"off_rev_{idx}")
            sostanza["fornitore_pa"] = st.text_input("Fornitore principio attivo", value=sostanza["fornitore_pa"], key=f"forn_rev_{idx}")
            sostanza["perc_attivo"] = st.text_input("% attivo", value=sostanza["perc_attivo"], key=f"perc_rev_{idx}")

        elif sostanza["stato_reg"] == "Approvato":
            idx_auth = 0 if sostanza.get("auth_biocida", "Sì") == "Sì" else 1
            sostanza["auth_biocida"] = st.radio("Ha ottenuto l'autorizzazione come biocida?", options=["Sì", "No"], index=idx_auth, horizontal=True, key=f"auth_{idx}")

            if sostanza["auth_biocida"] == "Sì":
                st.markdown(f"**Dati per la Sostanza #{idx + 1} - Biocida Autorizzato**")
                sostanza["titolare"] = st.text_input("Titolare", value=sostanza["titolare"], key=f"tit_app_{idx}")
                sostanza["nome_prodotto"] = st.text_input("Nome del prodotto", value=sostanza["nome_prodotto"], key=f"nprod_app_{idx}")
                sostanza["num_autorizzazione"] = st.text_input("Numero autorizzazione", value=sostanza["num_autorizzazione"], key=f"numauth_app_{idx}")
                sostanza["fornitore_pa"] = st.text_input("Fornitore principio attivo", value=sostanza["fornitore_pa"], key=f"forn_app_{idx}")

                sostanza["stati_membro"] = st.multiselect("Stati membri coinvolti nella valutazione", options=STATI_EUROPA, default=sostanza.get("stati_membro", []), key=f"statimem_{idx}")

                if sostanza["stati_membro"]:
                    st.caption("Specifica il ruolo per ogni Stato Membro selezionato:")
                    for stato in sostanza["stati_membro"]:
                        ruolo_corrente = sostanza["ruolo_stati"].get(stato, "Concerned")
                        idx_ruolo = 0 if ruolo_corrente == "Rapporteur" else 1
                        sostanza["ruolo_stati"][stato] = st.selectbox(f"Ruolo {stato}", options=["Rapporteur", "Concerned"], index=idx_ruolo, key=f"ruolo_{idx}_{stato}")

            else:
                st.markdown(f"**Dati per la Sostanza #{idx + 1} - Non Autorizzato**")
                sostanza["case_number"] = st.text_input("Case number", value=sostanza["case_number"], key=f"case_no_{idx}")
                st.markdown("*(Si prega di compilare i dati relativi alla revisione)*")
                sostanza["titolare"] = st.text_input("Titolare", value=sostanza["titolare"], key=f"tit_no_{idx}")
                sostanza["nome_prodotto"] = st.text_input("Nome prodotto", value=sostanza["nome_prodotto"], key=f"nprod_no_{idx}")
                sostanza["officina_produzione"] = st.text_input("Officina produzione", value=sostanza["officina_produzione"], key=f"off_no_{idx}")
                sostanza["fornitore_pa"] = st.text_input("Fornitore principio attivo", value=sostanza["fornitore_pa"], key=f"forn_no_{idx}")
                sostanza["perc_attivo"] = st.text_input("% attivo", value=sostanza["perc_attivo"], key=f"perc_no_{idx}")

        st.markdown("---")

        sostanza["pt"] = st.multiselect(f"PT di interesse Sostanza #{idx + 1}:", options=OPZIONI_PT, default=sostanza["pt"], key=f"pt_{idx}")
        idx_rischio = OPZIONI_BASSO_RISCHIO.index(sostanza["basso_rischio"]) if sostanza["basso_rischio"] in OPZIONI_BASSO_RISCHIO else 1
        sostanza["basso_rischio"] = st.radio(f"Basso rischio Sostanza #{idx + 1}?", options=OPZIONI_BASSO_RISCHIO, index=idx_rischio, horizontal=True, key=f"rischio_{idx}")

        if len(st.session_state.sostanze_list) > 1:
            st.button(f"🗑️ Rimuovi Sostanza #{idx + 1}", on_click=rimuovi_sostanza, args=(idx,), key=f"btn_del_{idx}")

st.button("➕ Aggiungi un'ulteriore sostanza attiva", on_click=aggiungi_sostanza, type="secondary")

st.divider()

# ==============================================================================
# 5. SCHEDA PRODOTTO E STABILIMENTO
# ==============================================================================
st.header("5. Scheda Prodotto e Stabilimento")
st.caption("Inserire i dati per ciascun prodotto Biocida o PMC.")

for idx_p, prod in enumerate(st.session_state.prodotti_list):
    titolo_p_expander = f"Prodotto #{idx_p + 1}: {prod['nome']}" if prod["nome"] else f"Prodotto #{idx_p + 1}"

    with st.expander(titolo_p_expander, expanded=(idx_p == 0)):
        cp1, cp2 = st.columns(2)
        with cp1:
            prod["nome"] = st.text_input(f"Nome Prodotto #{idx_p + 1}", value=prod["nome"], key=f"p_nome_{idx_p}")
        with cp2:
            idx_t_prod = OPZIONI_TIPO_PRODOTTO.index(prod["tipo"]) if prod["tipo"] in OPZIONI_TIPO_PRODOTTO else 0
            prod["tipo"] = st.selectbox(f"Inquadramento Prodotto #{idx_p + 1}", options=OPZIONI_TIPO_PRODOTTO, index=idx_t_prod, key=f"p_tipo_{idx_p}")

        prod["target"] = st.multiselect(
            f"Target spettro d'azione Prodotto #{idx_p + 1}",
            options=OPZIONI_TARGET,
            default=prod["target"],
            key=f"p_target_{idx_p}"
        )

        idx_form = OPZIONI_FORMULAZIONE.index(prod["formulazione"]) if prod["formulazione"] in OPZIONI_FORMULAZIONE else 0
        prod["formulazione"] = st.radio(
            f"Tipologia di formulazione Prodotto #{idx_p + 1}",
            options=OPZIONI_FORMULAZIONE,
            index=idx_form,
            horizontal=True,
            key=f"p_form_{idx_p}"
        )

        idx_conf = OPZIONI_CONFEZIONAMENTO.index(prod["confezionamento"]) if prod["confezionamento"] in OPZIONI_CONFEZIONAMENTO else 0
        prod["confezionamento"] = st.radio(
            f"Confezionamento Prodotto #{idx_p + 1}",
            options=OPZIONI_CONFEZIONAMENTO,
            index=idx_conf,
            horizontal=True,
            key=f"p_conf_{idx_p}"
        )

        prod["destinazione_uso"] = st.multiselect(
            f"Destinazione d'uso Prodotto #{idx_p + 1}",
            options=OPZIONI_DESTINAZIONE,
            default=prod["destinazione_uso"],
            key=f"p_dest_{idx_p}"
        )

        prod["utilizzatori"] = st.multiselect(
            f"Utilizzatori Prodotto #{idx_p + 1}",
            options=OPZIONI_UTILIZZATORI,
            default=prod["utilizzatori"],
            key=f"p_util_{idx_p}"
        )

        if len(st.session_state.prodotti_list) > 1:
            st.button(f"Rimuovi Prodotto #{idx_p + 1}", on_click=rimuovi_prodotto, args=(idx_p,), key=f"btn_del_p_{idx_p}")

st.button("➕ Aggiungi un altro prodotto", on_click=aggiungi_prodotto, type="secondary")

st.divider()

# ==============================================================================
# INVIO ED ESPORTAZIONE
# ==============================================================================
if st.button("Invia Questionario", type="primary", use_container_width=True):
    errori = []

    # Controlli Sede Titolare
    if not ambiti_tit:
        errori.append("Selezionare almeno un ambito per la Sede Titolare.")
    if "Italia" in ambiti_tit and (regione_tit == "Prego selezionare..." or provincia_tit == "Prego selezionare..."):
        errori.append("Completare Regione e Provincia per la Sede Italia Titolare.")
    if "Europa" in ambiti_tit and stato_eu_tit == "Prego selezionare...":
        errori.append("Selezionare lo Stato per la Sede Europa Titolare.")

    # Controlli Stabilimento
    if not ambiti_stab:
        errori.append("Selezionare almeno un'ubicazione per lo Stabilimento.")
    if "Italia" in ambiti_stab and (regione_stab == "Prego selezionare..." or provincia_stab == "Prego selezionare..."):
        errori.append("Completare Regione e Provincia per lo Stabilimento in Italia.")
    if "Europa" in ambiti_stab and stato_eu_stab == "Prego selezionare...":
        errori.append("Selezionare lo Stato per lo Stabilimento in Europa.")

    # Controllo che almeno la prima sostanza sia inserita
    sostanze_valide = [s for s in st.session_state.sostanze_list if s["nome"].strip()]
    if not sostanze_valide:
        errori.append("Inserire il Nome di almeno una Sostanza Attiva.")

    # Controllo che almeno un prodotto sia inserito
    prodotti_validi = [p for p in st.session_state.prodotti_list if p["nome"].strip()]
    if not prodotti_validi:
        errori.append("Inserire il Nome di almeno un Prodotto nella sezione 5.")

    if errori:
        for err in errori:
            st.error(f" {err}")
    else:
        st.success("Questionario inviato con successo!")

        # Generazione DataFrame Sostanze
        dati_sostanze = []
        for s in sostanze_valide:
            ruoli_str = "N/A"
            if s["stato_reg"] == "Approvato" and s["auth_biocida"] == "Sì" and s["stati_membro"]:
                ruoli_str = ", ".join([f"{stato} ({s['ruolo_stati'].get(stato, '')})" for stato in s["stati_membro"]])

            paese_prov_finale = s["paese_provenienza_eu"] if s["tipo_provenienza_mp"] == "Europa" else s["paese_provenienza_extra"]

            dati_sostanze.append({
                "Ambiti Sede Titolare": ", ".join(ambiti_tit),
                "Regione Sede Titolare": regione_tit,
                "Provincia Sede Titolare": provincia_tit,
                "Stato Europa Titolare": stato_eu_tit,
                "Ambiti Stabilimento": ", ".join(ambiti_stab),
                "Regione Stabilimento": regione_stab,
                "Provincia Stabilimento": provincia_stab,
                "Stato Europa Stabilimento": stato_eu_stab,
                "Produzione Fisica": prod_fisica,
                "Nome Sostanza": s["nome"],
                "CAS Number": s["cas"] or "N/A",
                "EC Number": s["ec"] or "N/A",
                "Origine Sostanza": s["origine"],
                "Specie Botanica": s["specie_botanica"] if s["origine"] == "Vegetale" else "N/A",
                "Parte Pianta": s["parte_pianta"] if s["origine"] == "Vegetale" else "N/A",
                "Provenienza MP (Tipo)": s["tipo_provenienza_mp"],
                "Paese Provenienza MP": paese_prov_finale or "N/A",
                "Stato Regolatorio PA": s["stato_reg"],
                "Auth Biocida": s["auth_biocida"] if s["stato_reg"] == "Approvato" else "N/A",
                "Case Number": s["case_number"] if (s["stato_reg"] == "Approvato" and s["auth_biocida"] == "No") else "N/A",
                "Titolare": s["titolare"],
                "Nome Prodotto": s["nome_prodotto"],
                "Officina Produzione": s["officina_produzione"],
                "Fornitore PA": s["fornitore_pa"],
                "% Attivo": s["perc_attivo"],
                "Num Autorizzazione": s["num_autorizzazione"] if (s["stato_reg"] == "Approvato" and s["auth_biocida"] == "Sì") else "N/A",
                "Stati Membri e Ruolo": ruoli_str,
                "PT Interesse": ", ".join(s["pt"]) if s["pt"] else "Nessuno",
                "Basso Rischio": s["basso_rischio"],
            })

        # Generazione DataFrame Prodotti
        dati_prodotti = []
        for p in prodotti_validi:
            dati_prodotti.append({
                "Nome Prodotto": p["nome"],
                "Inquadramento": p["tipo"],
                "Target Spettro": ", ".join(p["target"]) if p["target"] else "Nessuno",
                "Formulazione": p["formulazione"],
                "Confezionamento": p["confezionamento"],
                "Destinazione d'Uso": ", ".join(p["destinazione_uso"]) if p["destinazione_uso"] else "Nessuna",
                "Utilizzatori": ", ".join(p["utilizzatori"]) if p["utilizzatori"] else "Nessuno",
            })

        df_sostanze = pd.DataFrame(dati_sostanze)
        df_prodotti = pd.DataFrame(dati_prodotti)

        st.subheader("Tabella Sostanze Attive")
        st.dataframe(df_sostanze, use_container_width=True)

        st.subheader("Tabella Prodotti")
        st.dataframe(df_prodotti, use_container_width=True)

        # Download CSV / Excel
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                " Scarica CSV Sostanze",
                data=df_sostanze.to_csv(index=False).encode("utf-8"),
                file_name="sostanze.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_dl2:
            buffer_excel = io.BytesIO()
            with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
                df_sostanze.to_excel(writer, index=False, sheet_name="Sostanze Attive")
                df_prodotti.to_excel(writer, index=False, sheet_name="Prodotti")
            st.download_button(
                " Scarica Excel Completo (.xlsx)",
                data=buffer_excel.getvalue(),
                file_name="risposte_complete.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
