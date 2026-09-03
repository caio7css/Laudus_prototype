import streamlit as st
import os
import datetime


st.set_page_config(page_title="Laudus - Página Inicial", layout="wide")


if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.error(" Você não está autenticado. Por favor, faça login primeiro.")
    if st.button("Ir para Login"):
        st.switch_page("pages/pag_identificacao.py")
    st.stop()


def listar_templates(caminho_pasta):
    """Lista apenas os arquivos .docx (templates) de uma pasta de laudos,
    ignorando os PDFs de pré-visualização (convenção: NOME_pdf.pdf)."""
    if not os.path.isdir(caminho_pasta):
        return []
    return sorted(
        f for f in os.listdir(caminho_pasta)
        if os.path.isfile(os.path.join(caminho_pasta, f))
        and f.lower().endswith('.docx')
        and not f.startswith("~$")
    )


def exibir_pagina_inicial():

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**CRM:** {st.session_state.crm}")
    with col2:
        st.markdown(f"**Especialização:** {st.session_state.especializacao}")
    with col3:
        if st.button("Sair", use_container_width=True):
            st.session_state.logado = False
            st.switch_page("pages/pag_identificacao.py")

    st.title("Laudus - Sistema de Laudos")
    st.markdown("---")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.title("Seleção de exame: ")

        tipo_exame = st.selectbox("Selecione qual exame será realizado: ", ['Raio-x', 'Ultrassom', 'Tomografia'])

        # carrega os caminhos para a opção
        caminho_laudo_raiox = os.path.join(os.path.dirname(__file__), '../mascaras_laudos/Raio-x')
        caminho_laudo_tomografia = os.path.join(os.path.dirname(__file__), '../mascaras_laudos/Tomografia')
        caminho_laudo_ultrassom = os.path.join(os.path.dirname(__file__), '../mascaras_laudos/Ultrassom')

        raiosx = listar_templates(caminho_laudo_raiox)
        ultrassom = listar_templates(caminho_laudo_ultrassom)
        tomografia = listar_templates(caminho_laudo_tomografia)

        match tipo_exame:
            case "Raio-x":
                if raiosx:
                    rx_selecionado = st.selectbox("Tipo de Raio-x", raiosx)
                    st.session_state.rx = rx_selecionado
                    st.session_state.uts = None
                    st.session_state.tmf = None
                else:
                    st.info("Nenhum tipo de raio-x encontrado")

            case "Ultrassom":
                if ultrassom:
                    uts_selecionado = st.selectbox("Tipo de Ultrassom", ultrassom)
                    st.session_state.uts = uts_selecionado
                    st.session_state.rx = None
                    st.session_state.tmf = None
                else:
                    st.info("Nenhum tipo de ultrassom encontrada")

            case "Tomografia":
                if tomografia:
                    tmf_selecionado = st.selectbox("Tipo de Tomografia", tomografia)
                    st.session_state.tmf = tmf_selecionado
                    st.session_state.rx = None
                    st.session_state.uts = None
                else:
                    st.info("Nenhum tipo de tomografia encontrado")
    st.session_state.exame_selecionado = tipo_exame

    with col2:
        nome_paciente = st.text_input("Nome do Paciente ")
        st.session_state.nome_paciente = nome_paciente

        nascimento_paciente = st.date_input("Data de nascimento do paciente: ",
                                            min_value=datetime.date(1900, 1, 1),
                                            max_value=datetime.date(2100, 12, 31))
        st.session_state.nascimento_paciente = nascimento_paciente

        pronturario_paciente = st.text_input("Número do prontuário do paciente")
        st.session_state.prontuario_paciente = pronturario_paciente

        st.session_state.data_hoje = datetime.date.today()

        # Botão para ir para gravação
        if st.button("Ir para a página de gravação ->", use_container_width=True, type="primary"):
            if not nome_paciente or not pronturario_paciente:
                st.error("⚠️ Preencha o nome e o prontuário do paciente!")
            elif hasattr(st.session_state, 'rx') and st.session_state.rx:
                st.switch_page("pages/pag_gravar_audio.py")
            elif hasattr(st.session_state, 'uts') and st.session_state.uts:
                st.switch_page("pages/pag_gravar_ultrassom.py")
            elif hasattr(st.session_state, 'tmf') and st.session_state.tmf:
                st.switch_page("pages/pag_gravar_tomografia.py")
            else:
                st.error("⚠️ Selecione um tipo de exame primeiro!")

exibir_pagina_inicial()
