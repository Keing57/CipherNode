import tkinter as tk
from tkinter import scrolledtext, messagebox
from network import P2PNode

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P Chat")
        self.root.geometry("600x500")
        self.node = P2PNode()

        # Top Frame for Connection
        top_frame = tk.Frame(root)
        top_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(top_frame, text="IP:").pack(side=tk.LEFT)
        self.ip_entry = tk.Entry(top_frame, width=15)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(top_frame, text="Port:").pack(side=tk.LEFT)
        self.port_entry = tk.Entry(top_frame, width=8)
        self.port_entry.insert(0, "5000")
        self.port_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.connect_btn = tk.Button(top_frame, text="Connect")
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.host_btn = tk.Button(top_frame, text="Host", command=self.start_hosting)
        self.host_btn.pack(side=tk.LEFT)

        # Middle Frame for Chat
        chat_frame = tk.Frame(root)
        chat_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.chat_text = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True)

        # Bottom Frame for Input
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.msg_entry = tk.Entry(bottom_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.send_btn = tk.Button(bottom_frame, text="Send", width=10)
        self.send_btn.pack(side=tk.LEFT)

    def start_hosting(self):
        host = self.ip_entry.get()
        port_str = self.port_entry.get()
        if not port_str.isdigit():
            messagebox.showerror("Error", "Port must be a number")
            return
        port = int(port_str)
        
        self.host_btn.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.DISABLED)
        self.log_message(f"Waiting for connection on {host}:{port}...")
        
        self.node.start_hosting(host, port, self.on_connected)

    def on_connected(self):
        # Using root.after to safely update GUI from another thread
        self.root.after(0, lambda: self.log_message(f"Connected to {self.node.address}"))

    def log_message(self, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
