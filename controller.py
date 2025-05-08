from model import listaProcessos
from view import mostrarProcessos

def executarDashboard():
    processos = listaProcessos()
    mostrarProcessos(processos)