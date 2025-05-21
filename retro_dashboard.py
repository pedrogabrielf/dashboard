import streamlit as st
import psutil
import time
from model import listaProcessos

# Streamlit UI
st.set_page_config(
    page_title="Dashboard Retrô de Processos",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS retrô
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: black !important;
            color: #00FF00 !important;
            font-family: "Courier New", monospace;
        }
        .stProgress > div > div > div > div {
            background-color: #00FF00;
        }
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🟢 DASHBOARD RETRÔ DE PROCESSOS (Tempo Real)")

placeholder = st.empty()

# Loop de atualização
while True:
    with placeholder.container():
        processos = listaProcessos()
        tabela = [{
            "PID": p.pid,
            "Nome": p.name,
            "Estado": p.estado,
            "PPID": p.ppid,
            "UID": p.uid,
            "Threads": p.threads,
            "CPU (user ticks)": p.cpuUserTick,
            "CPU (kernel ticks)": p.cpuSysTick,
            "RAM (KB)": p.memoriaKB
        } for p in processos]

        st.dataframe(tabela, use_container_width=True)

    time.sleep(2)