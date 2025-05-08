from pathlib import Path

class Processo:
    def __init__(self, pid):
        self.pid = pid      # PID do proceso
        self.ppid = 0       # PID do processo pai
        self.estado = ''    # Estado (running, sleep, etc)
        self.uid = 0        # ID do usuário dono do processo
        self.cpuUserTick = 0 # Tempo de uso de CPU modo usuário
        self.cpuSysTick = 0  # Tempo de uso de CPU modo sistema
        self.threads = 0    # Threads do processo
        self.commandCMD = ''# Comando que iniciou o processo

    def iniciarProcesso(self):
        # Lógica para ler o processo
        print()

    def __repr__(self):
        return (f"<Processo PID={self.pid} PPID={self.ppid} Estado={self.estado} "
                f"UID={self.uid} CPU(User)={self.cpuUserTick} CPU(Sys)={self.cpuSysTick} "
                f"Threads={self.threads} CMD='{self.commandCMD}'>")
def imprimeArquivo(path):
    with open(path, 'r') as f:
            for linha in f:
                print(linha)

def cpuInfo():
    imprimeArquivo('/proc/cpuinfo')

def statusProcesso(PID):
    path = "/proc/" + str(PID) + "/status"
    imprimeArquivo(path)

def listaProcessos():
    proc = Path('/proc')
    PIDS = [int(p.name) for p in proc.iterdir() if p.is_dir() and p.name.isdigit()]
    print(sorted(PIDS))

generico = Processo(10)

print(generico)