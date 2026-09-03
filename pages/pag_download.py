import streamlit as st

st.set_page_config(page_title="Laudus - Download do Laudo", layout="centered")

if not st.session_state.get("logado"):
    st.error("Você não está autenticado. Por favor, faça login primeiro.")
    st.stop()

if not st.session_state.get("laudo_gerado"):
    st.error("Nenhum laudo foi gerado ainda.")
    if st.button("Voltar para a gravação"):
        st.switch_page("pages/pag_gravar_audio.py")
    st.stop()

st.title("✅ Laudo gerado com sucesso!")
st.markdown(f"**Paciente:** {st.session_state.get('nome_paciente', '')}")
st.markdown(f"**Prontuário:** {st.session_state.get('prontuario_paciente', '')}")
st.markdown(f"**Médico(a):** {st.session_state.get('nome_medico', '')} (CRM {st.session_state.get('crm', '')})")

st.markdown("---")

st.download_button(
    label="⬇️ Baixar Laudo (.docx)",
    data=st.session_state.laudo_gerado,
    file_name=st.session_state.get("laudo_nome_arquivo", "laudo.docx"),
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    use_container_width=True,
    type="primary",
)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("Fazer outro laudo", use_container_width=True):
        for chave in ("texto_transcrito", "laudo_gerado", "laudo_nome_arquivo"):
            st.session_state.pop(chave, None)
        st.switch_page("pages/pagina_inicial.py")
with col2:
    if st.button("Sair", use_container_width=True):
        st.session_state.logado = False
        st.switch_page("pages/pag_identificacao.py")
