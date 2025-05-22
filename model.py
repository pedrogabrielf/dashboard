# model.py
from pathlib import Path
import pwd
import time
import threading 

class Processo:
    def __init__(self, pid):
        self.pid = pid
        self.ppid = 0
        self.name = ''
        self.estado = ''
        self.uid = 0
        self.cpuUserTick = 0
        self.cpuSysTick = 0
        self.threads = 0
        self.commandCMD = ''
        self.memoriaKB = 0
        self.user = 'root'

    def cmdLine(self):
        try:
            cmd_path = f'/proc/{self.pid}/cmdline'
            with open(cmd_path, 'r') as f:
                conteudo = f.read()
                self.commandCMD = conteudo.replace('\x00', ' ').strip()
        except FileNotFoundError: # Capturar FileNotFoundError especificamente
            self.commandCMD = 'NO COMMAND (Processo encerrado)'
        except Exception as e: # Capturar outras exceções
            self.commandCMD = f'ERRO: {e}'

    def tempoDeCPU(self):
        path_cpu = f'/proc/{self.pid}/stat'
        try:
            with open(path_cpu, 'r') as f:
                valores = f.read().split()
                # Verifica se há valores suficientes antes de acessar os índices
                if len(valores) > 14:
                    self.cpuUserTick = int(valores[13])
                    self.cpuSysTick = int(valores[14])
                else:
                    self.cpuUserTick = 0 # ou outro valor padrão
                    self.cpuSysTick = 0 # ou outro valor padrão
        except FileNotFoundError:
            self.cpuUserTick = 0
            self.cpuSysTick = 0
        except Exception as e:
            print(f"Erro ao ler tempo de CPU para PID {self.pid}: {e}")
            self.cpuUserTick = 0
            self.cpuSysTick = 0

    def statusProcesso(self):
        status_path = f'/proc/{self.pid}/status'
        try:
            with open(status_path, 'r') as f:
                for linha in f:
                    if linha.startswith("Name:"):
                        self.name = linha.split()[1]
                    elif linha.startswith("PPid:"):
                        self.ppid = int(linha.split()[1])
                    elif linha.startswith("Uid:"):
                        self.uid = int(linha.split()[1])
                        try: # Tenta obter o nome do usuário
                            self.user = pwd.getpwuid(self.uid).pw_name
                        except KeyError: # Se o UID não for encontrado (ex: processo de sistema sem usuário tradicional)
                            self.user = f'UID:{self.uid}'
                    elif linha.startswith("State:"):
                        self.estado = linha.split()[1]
                    elif linha.startswith("Threads:"):
                        self.threads = int(linha.split()[1])
                    elif linha.startswith("VmRSS:"):
                        self.memoriaKB = int(linha.split()[1])
        except FileNotFoundError:
            self.name = '[Encerrado]'
            self.estado = 'Z'
            self.ppid = 0
            self.uid = -1
            self.threads = 0
            self.memoriaKB = 0
            self.user = '[Desconhecido]'
        except Exception as e:
            print(f"Erro ao ler status do processo {self.pid}: {e}")
            # Lidar com outros erros de leitura
            self.name = '[Erro]'

    def iniciarProcesso(self):
        self.statusProcesso()
        # Somente tenta ler CPU e CMD se o processo não estiver marcado como encerrado/erro
        if self.name not in ['[Encerrado]', '[Erro]']:
            self.tempoDeCPU()
            self.cmdLine()

    def __repr__(self):
        return (
        f"┌─ Processo PID={self.pid}\n"
        f"│  Nome        : {self.name}\n"
        f"│  Estado      : {self.estado}\n"
        f"│  PPID        : {self.ppid}\n"
        f"│  UID         : {self.uid}\n"
        f"│  Threads     : {self.threads}\n"
        f"│  CPU (User)  : {self.cpuUserTick} ticks\n"
        f"│  CPU (Kernel): {self.cpuSysTick} ticks\n"
        f"│  Memória RAM : {self.memoriaKB} kB\n"
        f"│     Usuário     : {self.user}\n"
        f"│  Comando     : {self.commandCMD}\n"
        f"└────────────────────────────────────────────"
    )

def uso_cpu_percent():
    def ler_cpu():
        try:
            with open("/proc/stat", "r") as f:
                linha = f.readline()
                campos = list(map(int, linha.strip().split()[1:]))
                total = sum(campos)
                idle = campos[3]
                return total, idle
        except FileNotFoundError:
            print("Erro: /proc/stat não encontrado.")
            return 0, 0
        except Exception as e:
            print(f"Erro ao ler /proc/stat: {e}")
            return 0, 0

    return 0.0, 0.0

def info_memoria():
    info = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for linha in f:
                partes = linha.split()
                if len(partes) > 1: # Garante que a linha tem partes suficientes
                    chave = partes[0].rstrip(":")
                    try:
                        valor = int(partes[1])
                        info[chave] = valor
                    except ValueError:
                        continue # Ignora linhas com valor não numérico
        
        mem_total = info.get('MemTotal', 0)
        # Buffers e Cached podem ou não existir, ou ser 0
        mem_livre = info.get('MemFree', 0) + info.get('Buffers', 0) + info.get('Cached', 0)
        mem_usada = mem_total - mem_livre
        mem_percent = 100 * (mem_usada / mem_total) if mem_total > 0 else 0
        livre_percent = 100 - mem_percent

        swap_total = info.get('SwapTotal', 0)
        swap_usada = swap_total - info.get('SwapFree', 0) if swap_total > 0 else 0

        return {
            "mem_total": mem_total,
            "mem_usada": mem_usada,
            "mem_livre_percent": livre_percent,
            "mem_usada_percent": mem_percent,
            "swap_total": swap_total,
            "swap_usada": swap_usada
        }
    except FileNotFoundError:
        print("Erro: /proc/meminfo não encontrado.")
        return {}
    except Exception as e:
        print(f"Erro ao ler /proc/meminfo: {e}")
        return {}


def total_processos_threads():
    total_threads = 0
    total_processos = 0

    proc = Path('/proc')
    try:
        for p in proc.iterdir():
            if p.is_dir() and p.name.isdigit():
                total_processos += 1
                try:
                    with open(p / "status", "r") as f:
                        for linha in f:
                            if linha.startswith("Threads:"):
                                total_threads += int(linha.split()[1])
                                break
                except FileNotFoundError:
                    continue # Processo pode ter terminado entre a listagem e a leitura
                except Exception as e:
                    print(f"Erro ao ler threads do processo {p.name}: {e}")
                    continue
    except Exception as e:
        print(f"Erro ao listar diretórios em /proc: {e}")
        return 0, 0

    return total_processos, total_threads

def listaProcessos():
    lista = []
    proc = Path('/proc')
    PIDS = [int(p.name) for p in proc.iterdir() if p.is_dir() and p.name.isdigit()]
    for pid in PIDS:
        p = Processo(pid)
        p.iniciarProcesso()
        # Opcional: filtrar processos que não foram encontrados (encerrados)
        if p.name != '[Encerrado]':
            lista.append(p)
    return lista


# NOVA CLASSE PARA O MODELO GERAL DO SISTEMA
class SystemMonitorModel:
    def __init__(self):
        self._data = {} # Dicionário para armazenar os dados coletados
        self._lock = threading.Lock() # Lock para garantir acesso seguro aos dados
        self._last_cpu_total = 0 # Para cálculo do uso de CPU%
        self._last_cpu_idle = 0  # Para cálculo do uso de CPU%

    def _get_raw_cpu_times(self):
        # Função interna para ler os tempos brutos da CPU
        try:
            with open("/proc/stat", "r") as f:
                linha = f.readline()
                campos = list(map(int, linha.strip().split()[1:]))
                total = sum(campos)
                idle = campos[3]
                return total, idle
        except (FileNotFoundError, IndexError, ValueError) as e:
            print(f"Erro ao ler /proc/stat: {e}")
            return 0, 0

    def _calculate_cpu_percentage(self):
        current_total, current_idle = self._get_raw_cpu_times()

        total_diff = current_total - self._last_cpu_total
        idle_diff = current_idle - self._last_cpu_idle

        # Atualiza os últimos valores para a próxima iteração
        self._last_cpu_total = current_total
        self._last_cpu_idle = current_idle

        if total_diff > 0:
            usage_percent = 100.0 * (total_diff - idle_diff) / total_diff
            idle_percent = 100.0 - usage_percent
            return usage_percent, idle_percent
        return 0.0, 100.0 # Se não houver mudança ou erro, assumir 0% uso

    def _collect_all_data(self):
        # Este método será executado pela thread em segundo plano
        temp_data = {}

        # Coleta de CPU global
        temp_data["cpu_usage"], temp_data["cpu_idle"] = self._calculate_cpu_percentage()

        # Coleta de memória global
        temp_data["mem_info"] = info_memoria()

        # Coleta de total de processos e threads
        temp_data["total_processes"], temp_data["total_threads"] = total_processos_threads()

        # Coleta da lista de processos detalhada
        temp_data["processes_list"] = listaProcessos()

        with self._lock:
            self._data = temp_data

    def get_dashboard_data(self):
        # Inicializa as leituras de CPU na primeira chamada
        if self._last_cpu_total == 0:
            self._last_cpu_total, self._last_cpu_idle = self._get_raw_cpu_times()
            # Pequeno delay para ter uma segunda leitura significativa
            time.sleep(0.1) # Pode ser ajustado ou removido se o autorefresh for > 1s

        # Inicia uma thread para coletar os dados
        collection_thread = threading.Thread(target=self._collect_all_data)
        collection_thread.start()
        collection_thread.join() # Espera a thread terminar a coleta

        # Retorna uma cópia dos dados coletados para segurança
        with self._lock:
            return self._data.copy()