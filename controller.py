import model
system_monitor_model = model.SystemMonitorModel()

def executarDashboard():
    """
    Função principal do Controller que orquestra a obtenção de dados
    e a atualização da View.
    """
    #    O Modelo gerencia a coleta em uma thread interna.
    dashboard_data = system_monitor_model.get_dashboard_data()

    import view # Importe a view aqui, ou ajuste a estrutura do Streamlit
    view.render_dashboard(dashboard_data) # Chama a função da View para renderizar