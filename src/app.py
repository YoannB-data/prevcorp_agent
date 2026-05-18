"""Application Streamlit pour l'agent PrevCorp."""

import streamlit as st

from src.agent import agent_main
from src.chart_utils import try_build_chart

st.set_page_config(page_title="PrevCorp Agent", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("PrevCorp Agent")
st.subheader("Votre question")

question = st.text_area("", placeholder="Ex : Combien de dossiers ouverts en 2024 ?", height=100)

if st.button("Envoyer", type="primary", disabled=not question.strip()):
    try:
        with st.spinner("Requête en cours…"):
            sql, result_df  = agent_main(question)
        st.session_state.history.insert(0, {"question": question, "sql": sql, "result": result_df})
    except Exception as e:
        st.error(f"Erreur lors de l'exécution : {e}")

st.divider()

for entry in st.session_state.history:
    st.markdown(f"**{entry['question']}**")
    st.code(entry["sql"], language="sql")
    st.dataframe(entry["result"], use_container_width=True)
    fig = try_build_chart(entry["result"])
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
