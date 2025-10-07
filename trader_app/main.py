import threading
import tkinter as tk
from src.terminal.terminal_screen import RoundedTerminal
from src.data.data_search import MegaTraderCSV
from src.terminal.send.sender import send, sendMessage

def run_data_tasks():
    sendMessage("⏳ Iniciando geração de CSVs históricos...")
    MegaTraderCSV.generate()
    sendMessage("✅ Geração de CSVs finalizada!")

root = tk.Tk()
terminal_app = RoundedTerminal(root)

send.bind_terminal(terminal_app.terminal)
sendMessage("✅ Terminal iniciado com sucesso!")

data_thread = threading.Thread(target=run_data_tasks, daemon=True)
data_thread.start()

root.mainloop()
