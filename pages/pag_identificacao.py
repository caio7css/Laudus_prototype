import os
import sqlite3
import sys

import streamlit as st

# Garante que a raiz do projeto (onde fica inicializar_banco.py) esteja no path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from inicializar_banco import inicializar_banco, CAMINHO_DB  # noqa: E402

st.set_page_config(page_title="Laudus - Identificação", layout="centered")


def conectar_banco():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect(CAMINHO_DB)


def validar_medico(crm, senha):
    """Valida o CRM e a senha, verificando acesso a exames de imagem.

    Retorna (valido, medico_id, especializacao, nome).
    """
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT id, nome, especializacao, acesso_exames_imagem FROM medicos WHERE crm = ? AND senha = ?',
            (crm, senha)
        )
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            medico_id, nome, especializacao, acesso_exames = resultado
            if acesso_exames:
                return True, medico_id, especializacao, nome
            else:
                return False, None, None, None
        else:
            return False, None, None, None
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return False, None, None, None


def login_medico():
    col1, col2, col3 = st.columns(3)

    st.title("Esta é a página de :green[Login]")
    st.subheader("Inserir seu CRM e a senha associada ao mesmo.", divider="blue")

    with col2:
        entrada_crm = st.text_input("Digite seu CRM: ")
        senha = st.text_input("Senha: ", type="password")

        if st.button("Realizar Login", use_container_width=True):
            if entrada_crm and senha:
                valido, medico_id, especializacao, nome = validar_medico(entrada_crm, senha)

                if valido:
                    st.session_state.logado = True
                    st.session_state.crm = entrada_crm
                    st.session_state.medico_id = medico_id
                    st.session_state.especializacao = especializacao
                    st.session_state.nome_medico = nome
                    st.success(f"Bem-vindo(a), {nome}! Especialização: {especializacao}")
                    st.switch_page("pages/pagina_inicial.py")
                else:
                    st.error("CRM ou senha inválidos, ou você não tem permissão para acessar exames de imagem.")
            else:
                st.error("Preencha todos os dados.")


inicializar_banco()
login_medico()
