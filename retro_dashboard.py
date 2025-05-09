import streamlit as st
import psutil
import time

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

# Loop de atualização em tempo real
while True:
    with placeholder.container():
        processes = list(psutil.process_iter())
        processes.sort(key=lambda p: p.pid)
        table = []
        for p in processes:
            try:
                with p.oneshot():
                    table.append({
                        "PID": p.pid,
                        "Nome": p.name(),
                        "Status": p.status(),
                        "PPID": p.ppid(),
                        "UID": p.uids().real if hasattr(p, "uids") else "N/A",
                        "Threads": p.num_threads(),
                        "CPU (user)": f"{p.cpu_times().user:.1f}",
                        "CPU (kernel)": f"{p.cpu_times().system:.1f}",
                        "RAM (KB)": f"{p.memory_info().rss // 1024}"
                    })
            except Exception:
                continue

        st.dataframe(table, use_container_width=True)

    time.sleep(2)  # Atualiza a cada 2 segundos
