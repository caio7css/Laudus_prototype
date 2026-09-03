import streamlit as st

st.set_page_config(page_title="Laudus ", layout="centered")

st.title("Bem-vindo ao :blue[Laudus]")
st.subheader("Sistema de automação para Laudos Médicos em Exames de Imagem", divider="blue")

st.markdown("""
### Sobre o Sistema
O Laudus é um sistema que digitaliza automaticamente os laudos médicos para exames de imagem.

**Como utilizar:**
-  Identifique-se.
-  Selecione o exame que irá realizar.
-  Preencha as informações básicas do paciente.
-  Dite o resultado seguindo as instruções que serão exibidas posteriormente.
-  Corrija o resultado se necessário.
-  Envie o resultado.

""")

col1, col2, col3 = st.columns(3)

with col2:
    if st.button("Ir para Login", use_container_width=True, key="login_button"):
        st.switch_page("pages/pag_identificacao.py")

st.markdown("---")
st.markdown("**Médicos com acesso disponível:**")
st.markdown("""
- Milena Veiga | CRM: 345678 | Senha: senha345 | Radiologia
(este trata-se de uma versão beta, o login válido aqui é exibido apenas com o fito de demonstrar o funcionamento.)
""")
