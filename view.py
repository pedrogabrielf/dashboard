# view.py (antigo streamlit_dashboard.py)
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Importe o controller, mas não chame o model aqui diretamente.
# A função de renderização será chamada pelo controller.

# Funções da View devem receber os dados como argumento
def render_dashboard(data):
    # Configurações da página (pode ser movido para fora da função se Streamlit permitir)
    st.set_page_config(
        page_title="Dashboard de Processos",
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
        .stats-box {
            border: 2px solid #00FF00;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("DASHBOARD DE PROCESSOS Pedro & Vitor")

    # ⏱Atualiza a cada 2 segundos
    # Esta linha faz com que o Streamlit re-execute TODO o script 'main.py'
    # que por sua vez chama o Controller para coletar e passar os dados.
    st_autorefresh(interval=2000, key="atualiza")

    # OBTENDO DADOS DO DICIONÁRIO 'data' RECEBIDO DO CONTROLLER
    uso_cpu = data.get('cpu_usage', 0)
    ocioso_cpu = data.get('cpu_idle', 0)
    mem_info = data.get('mem_info', {})
    total_proc = data.get('total_processes', 0)
    total_thr = data.get('total_threads', 0)
    processes_list = data.get('processes_list', [])

    # Layout em colunas para estatísticas do sistema
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="stats-box">', unsafe_allow_html=True)
        st.markdown("### 💻 CPU")
        st.progress(uso_cpu/100)
        st.write(f"Uso da CPU: **{uso_cpu:.2f}%**")
        st.write(f"CPU Ociosa: **{ocioso_cpu:.2f}%**")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stats-box">', unsafe_allow_html=True)
        st.markdown("### 🧠 Memória")
        # Lidar com casos onde mem_info pode estar vazio
        mem_usada_percent = mem_info.get('mem_usada_percent', 0)
        mem_usada_mb = mem_info.get('mem_usada', 0) / 1024
        mem_livre_percent = mem_info.get('mem_livre_percent', 0)
        mem_total_mb = mem_info.get('mem_total', 0) / 1024

        st.progress(mem_usada_percent/100)
        st.write(f"Memória Usada: **{mem_usada_percent:.2f}%** ({mem_usada_mb:.1f} MB)")
        st.write(f"Memória Livre: **{mem_livre_percent:.2f}%**")
        st.write(f"Total RAM: **{mem_total_mb:.1f} MB**")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="stats-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Processos")
        swap_usada_mb = mem_info.get('swap_usada', 0) / 1024
        swap_total_mb = mem_info.get('swap_total', 0) / 1024
        
        st.write(f"Total de Processos: **{total_proc}**")
        st.write(f"Total de Threads: **{total_thr}**")
        st.write(f"SWAP Usado: **{swap_usada_mb:.1f} MB** / **{swap_total_mb:.1f} MB**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Adicionar uma linha de separação
    st.markdown("---")

    # Título da seção de processos
    st.markdown("### 📋 Lista de Processos")

    # Lista de processos (já veio pré-processada do Modelo via Controller)
    processes_list.sort(key=lambda p: p.pid)

    # Tabela formatada
    table = [{
        "PID": p.pid,
        "Nome": p.name,
        "Status": p.estado,
        "PPID": p.ppid,
        "UID": p.uid,
        "Threads": p.threads,
        "CPU (user)": p.cpuUserTick,
        "CPU (kernel)": p.cpuSysTick,
        "RAM (KB)": p.memoriaKB,
        "Usuário": p.user,
        "Comando": p.commandCMD
    } for p in processes_list]

    st.dataframe(table, use_container_width=True)

    # Adicionar contador de processos
    st.write(f"Total de processos exibidos: {len(processes_list)}")

    # Adicionar rodapé
    st.markdown("---")
    st.caption("Dashboard de Processos - Sistemas Operacionais UTFPR")