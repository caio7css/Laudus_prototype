import os
import tempfile

import streamlit as st
from faster_whisper import WhisperModel

PROMPT_PADRAO = (
    "Transparência pulmonar, Seios costofrênicos, Mediastino, "
    "Índice cardiotorácico, Estruturas ósseas"
)


@st.cache_resource
def carrega_whisper(tamanho_modelo: str = "small"):
    """Carrega o modelo Whisper uma única vez (cacheado em memória/RAM)."""
    return WhisperModel(tamanho_modelo, device="cpu", compute_type="int8")


def transcreve(audio_bytes, prompt_contexto: str = "") -> str:
    """Processa o buffer de áudio (retorno de st.audio_input) e retorna a transcrição."""
    if not audio_bytes:
        return ""

    caminho_temp = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes.getvalue())
            caminho_temp = tmp_file.name

        modelo = carrega_whisper()

        if not prompt_contexto:
            prompt_contexto = PROMPT_PADRAO

        segments, _info = modelo.transcribe(
            caminho_temp,
            language="pt",
            beam_size=5,
            initial_prompt=prompt_contexto,
            vad_filter=True,
        )

        texto_transcrito = " ".join(segment.text.strip() for segment in segments)
        return texto_transcrito.strip()

    except Exception as e:
        st.error(f"Erro ao transcrever o áudio: {e}")
        return ""

    finally:
        if caminho_temp and os.path.exists(caminho_temp):
            os.remove(caminho_temp)
