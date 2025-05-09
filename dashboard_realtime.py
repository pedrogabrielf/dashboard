import curses
import psutil
import time
import os

def format_process(p):
    try:
        with p.oneshot():
            pid = p.pid
            name = p.name()
            status = p.status()
            ppid = p.ppid()
            uid = p.uids().real if hasattr(p, 'uids') else "N/A"
            threads = p.num_threads()
            cpu_user = p.cpu_times().user
            cpu_sys = p.cpu_times().system
            mem = p.memory_info().rss // 1024  # kB
            return f"PID={pid} | Nome={name} | Estado={status} | PPID={ppid} | UID={uid} | Threads={threads} | CPU User={cpu_user:.1f} | CPU Kernel={cpu_sys:.1f} | RAM={mem} KB"
    except Exception:
        return None

def draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    delay = 1  # segundos

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "╔════════════════════════════════════════════════════╗")
        stdscr.addstr(1, 0, "║       DASHBOARD DE PROCESSOS (TEMPO REAL)         ║")
        stdscr.addstr(2, 0, "╚════════════════════════════════════════════════════╝")

        processes = [p for p in psutil.process_iter()]
        processes.sort(key=lambda p: p.pid)

        row = 4
        for p in processes:
            info = format_process(p)
            if info:
                try:
                    stdscr.addstr(row, 0, info[:curses.COLS - 1])
                    row += 1
                    if row >= curses.LINES - 1:
                        break
                except curses.error:
                    pass  # ignora erros ao escrever fora da tela

        stdscr.refresh()
        time.sleep(delay)

        if stdscr.getch() == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(draw_dashboard)
