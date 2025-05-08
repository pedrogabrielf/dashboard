from pathlib import Path

class Processo:
    def __init__(self, pid):
        self.pid = pid       # PID do proceso
        self.ppid = 0        # PID do processo pai
        self.name = ''       # Nome do processo
        self.estado = ''     # Estado (running, sleep, etc)
        self.uid = 0         # ID do usuário dono do processo
        self.cpuUserTick = 0 # Tempo de uso de CPU modo usuário
        self.cpuSysTick = 0  # Tempo de uso de CPU modo sistema
        self.threads = 0     # Threads do processo
        self.commandCMD = '' # Comando que iniciou o processo

    def iniciarProcesso(self):
        status_path = '/proc/' + str(self.pid) + '/status'
        try:
            with open(status_path, 'r') as f:
                for linha in f:
                    if linha.startswith("Name:"):
                        self.name = linha.split()[1]
                    elif linha.startswith("PPid:"):
                        self.ppid = int(linha.split()[1])
                    elif linha.startswith("Uid:"):
                        self.uid = int(linha.split()[1])
                    elif linha.startswith("State:"):
                        self.estado = linha.split()[1]
                    elif linha.startswith("Threads:"):
                        self.threads = int(linha.split()[1])
                    # Se já tiver todos os campos, pode parar cedo (opcional)
                    if all([self.name, self.ppid, self.estado, self.uid, self.threads]):
                        break
        except FileNotFoundError:
            print(f"Processo {self.pid} não encontrado.")
            

    def __repr__(self):
        return (f"Processo {self.name} PID={self.pid} PPID={self.ppid} Estado={self.estado} "
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


teste = Processo(100)

teste.iniciarProcesso()
print(teste)