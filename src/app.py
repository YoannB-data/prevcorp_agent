"""Application Streamlit pour l'agent PrevCorp."""

import json

import streamlit as st

from src.agent import agent_main
from src.chart_utils import try_build_chart
from src.config import LATEST_EVAL_PATH

st.set_page_config(page_title="PrevCorp Agent", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("Assistant PrevCorp")
    st.subheader("Interrogez vos données en langage naturel")
    st.divider()
    if LATEST_EVAL_PATH.exists():
        eval_data = json.loads(LATEST_EVAL_PATH.read_text(encoding="utf-8"))
        st.metric("Score eval set", f"{eval_data['score_pct']}%")
        st.caption(
            f"{eval_data['passed']}/{eval_data['evaluated']} PASS"
            f" · {eval_data['date'][:10]}"
        )
    else:
        st.caption("_Aucune évaluation disponible_")
    st.divider()
    st.metric("Questions posées", len(st.session_state.history))
    if st.button("Effacer l'historique"):
        st.session_state.history = []
        st.rerun()
    st.divider()
    st.caption("Dataset PrevCorp · 2022–2025")
    st.caption("~2 000 assurés")
    st.caption("~3 000 contrats")
    st.caption("~1 500 sinistres")

st.divider()

for entry in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(entry["question"])
    # st.code(entry["sql"], language="sql")
    st.dataframe(entry["result"], use_container_width=True)
    fig = try_build_chart(entry["result"])
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

if question := st.chat_input("Ex : Combien de dossiers ouverts en 2024 ?"):
    try:
        with st.spinner("Requête en cours…"):
            sql, result_df = agent_main(question)
            st.session_state.history.append(
                {"question": question, "sql": sql, "result": result_df}
            )
        st.rerun()
    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Erreur lors de l'exécution : {e}")
