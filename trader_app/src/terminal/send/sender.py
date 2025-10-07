import tkinter as tk

class SenderService:

    def __init__(self):
        self.terminal = None
        self.queue = []

    def bind_terminal(self, terminal_widget: tk.Text):
        self.terminal = terminal_widget
        self.terminal.config(state='normal')

        for msg in self.queue:
            self._send_to_terminal(msg)
        self.queue.clear()
        self.terminal.config(state='disabled')

    def _send_to_terminal(self, msg: str):
        if not self.terminal:
            self.queue.append(msg)
            print(msg)
            return
        self.terminal.config(state='normal')
        self.terminal.insert('end', msg + '\n')
        self.terminal.see('end')
        self.terminal.config(state='disabled')

    def service_message(self, msg: str):
        if self.terminal:
            self._send_to_terminal(msg)
        else:
            self.queue.append(msg)
            print(msg)

send = SenderService()

def sendMessage(msg: str):
    send.service_message(msg)
