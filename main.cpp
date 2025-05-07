#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>

void listaTarefas();
void leInformacoesDoProcesso(int PID);
namespace fs = std::filesystem;

class Processo {
private:
    std::string nome;   // Nome do processo
    int PID;            // PID
    int PPID;           // PID da tarefa pai
    char estado;        // Estado (R = running, S = sleeping...)
    int uid;            // Usuário dono da tarefa
    long cpuUserTicks;  // Tempo de uso de CPU no modo usuário
    long cpuSysTicks;   // Tempo de uso de CPU no modo sistema
    int threads;        // Threads do programam
    std::string comandoCMD; // Comando que iniciou a tarefa
public:
    Processo();
    ~Processo();
};


int main()
{
    // listaTarefas();
    leInformacoesDoProcesso(938);
}

void listaTarefas()
{
    fs::path diretorio = "/proc/";

    for(const auto &entrada : fs::directory_iterator(diretorio)){
        std::cout << entrada.path() << std::endl;
    }

    return;
}

void leInformacoesDoProcesso(int PID)
{
    fs::path processo = "/proc/" + std::to_string(PID);

    if(!fs::exists(processo)){
        std::cerr << "Processo " << PID << " nao existe" << std::endl;
        return;
    }

    fs::path statusProcesso = "/proc/" + std::to_string(PID) + "/status";
    std::ifstream arquivo(statusProcesso);
    
    std::string linha;
    while(std::getline(arquivo, linha)){
        std::cout << linha << std::endl;
    }

    arquivo.close();
}