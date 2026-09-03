import os
import sys

import streamlit as st
import fitz  # PyMuPDF

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.transcricao import transcreve  # noqa: E402
from utils.gerador_docx import extrair_secoes, gerar_laudo, caminho_preview_pdf  # noqa: E402

st.set_page_config(page_title="Laudus - Gravação de Áudio", layout="wide")

if not st.session_state.get("logado"):
    st.error("Você não está autenticado. Por favor, faça login primeiro.")
    st.stop()

if not st.session_state.get("rx"):
    st.error("Nenhum exame selecionado. Volte e selecione um exame primeiro.")
    if st.button("Voltar"):
        st.switch_page("pages/pagina_inicial.py")
    st.stop()

PLACEHOLDERS_DO_ARQUIVO = [
    "Transparência pulmonar",
    "Seios costofrênicos",
    "Mediastino",
    "Índice cardiotorácico",
    "Estruturas ósseas",
]

if "texto_transcrito" not in st.session_state:
    st.session_state.texto_transcrito = ""

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Os placeholders que você deverá utilizar são: ")
    for i in PLACEHOLDERS_DO_ARQUIVO:
        st.write(i)
        st.divider()

with col2:
    caminho_docx = os.path.join(
        os.path.dirname(__file__), '../mascaras_laudos/Raio-x', st.session_state.rx
    )
    caminho_pdf_preview = caminho_preview_pdf(caminho_docx)

    if os.path.exists(caminho_pdf_preview):
        st.write("Modelo do Laudo que será feito")
        try:
            pdf_document = fitz.open(caminho_pdf_preview)
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
                image_bytes = pix.tobytes("ppm")
                st.image(image_bytes, caption=f"Página {page_num + 1}", use_container_width=True)
            pdf_document.close()
        except Exception as e:
            st.error(f"Erro ao carregar PDF: {e}")
    else:
        st.info("Pré-visualização não encontrada para este modelo.")

with col3:
    audio_da_entrada = st.audio_input(
        "Fale pausadamente, alto e claro. Ao falar o nome do placeholder, "
        "diga-o mais alto e dê uma pequena pausa antes de citar o achado."
    )

    if audio_da_entrada:
        st.audio(audio_da_entrada)

        if st.button("Transcrever áudio", use_container_width=True):
            with st.spinner("Transcrevendo..."):
                texto = transcreve(audio_da_entrada)
            if texto:
                st.session_state.texto_transcrito = texto
            else:
                st.warning("Não foi possível transcrever o áudio. Tente novamente.")

st.markdown("---")

if st.session_state.texto_transcrito:
    st.subheader("Texto transcrito — revise e corrija antes de confirmar")
    texto_editado = st.text_area(
        "Você pode editar livremente o texto abaixo. Ele será usado para gerar o laudo.",
        value=st.session_state.texto_transcrito,
        height=200,
        key="texto_transcrito",
    )

    if st.button("Confirmar e Gerar Laudo ✅", type="primary", use_container_width=True):
        secoes = extrair_secoes(texto_editado, PLACEHOLDERS_DO_ARQUIVO)

        dados_paciente = {
            "nome": st.session_state.get("nome_paciente", ""),
            "prontuario": st.session_state.get("prontuario_paciente", ""),
            "nascimento": st.session_state.get("nascimento_paciente").strftime("%d/%m/%Y")
                if st.session_state.get("nascimento_paciente") else "",
            "data_realizacao": st.session_state.get("data_hoje").strftime("%d/%m/%Y")
                if st.session_state.get("data_hoje") else "",
        }

        medico = {
            "nome": st.session_state.get("nome_medico", ""),
            "crm": st.session_state.get("crm", ""),
            "uf": "PB",
        }

        try:
            laudo_bytes = gerar_laudo(
                caminho_template=caminho_docx,
                dados_paciente=dados_paciente,
                secoes=secoes,
                placeholders=PLACEHOLDERS_DO_ARQUIVO,
                medico=medico,
            )
            st.session_state.laudo_gerado = laudo_bytes.read()
            nome_base = os.path.splitext(st.session_state.rx)[0]
            nome_paciente_slug = (dados_paciente["nome"] or "paciente").strip().replace(" ", "_")
            st.session_state.laudo_nome_arquivo = f"{nome_base}_{nome_paciente_slug}.docx"
            st.switch_page("pages/pag_download.py")
        except Exception as e:
            st.error(f"Erro ao gerar o laudo: {e}")
else:
    st.info("Grave o áudio e clique em **Transcrever áudio** para continuar.")
