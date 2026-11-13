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

        self.connect_btn = tk.Button(top_frame, text="Connect", command=self.start_connecting)
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

        self.msg_entry = tk.Entry(bottom_frame, state=tk.DISABLED)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(bottom_frame, text="Send", width=10, command=self.send_message, state=tk.DISABLED)
        self.send_btn.pack(side=tk.LEFT)

    def get_host_port(self):
        host = self.ip_entry.get()
        port_str = self.port_entry.get()
        if not port_str.isdigit():
            messagebox.showerror("Error", "Port must be a number")
            return None, None
        return host, int(port_str)

    def start_hosting(self):
        host, port = self.get_host_port()
        if not host or not port: return
        
        self.host_btn.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.DISABLED)
        self.log_message(f"Waiting for connection on {host}:{port}...")
        
        self.node.start_hosting(host, port, self.on_connected, self.on_error, self.on_message_received, self.on_disconnected)

    def start_connecting(self):
        host, port = self.get_host_port()
        if not host or not port: return
        
        self.host_btn.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.DISABLED)
        self.log_message(f"Connecting to {host}:{port}...")
        
        self.node.connect_to_host(host, port, self.on_connected, self.on_error, self.on_message_received, self.on_disconnected)

    def on_connected(self):
        self.root.after(0, lambda: self.enable_chat_input())
        self.root.after(0, lambda: self.log_message(f"Connected to {self.node.address}"))

    def enable_chat_input(self):
        self.msg_entry.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        self.host_btn.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.DISABLED)

    def on_error(self, err_msg):
        self.root.after(0, lambda: self.reset_buttons())
        self.root.after(0, lambda: messagebox.showerror("Connection Error", err_msg))
        self.root.after(0, lambda: self.log_message(f"Error: {err_msg}"))
        
    def on_disconnected(self):
        self.root.after(0, lambda: self.reset_buttons())
        self.root.after(0, lambda: self.log_message("Connection Lost"))

    def on_message_received(self, message):
        self.root.after(0, lambda: self.log_message(f"Peer: {message}"))

    def send_message(self):
        # Even if enter is pressed, check if entry is disabled
        if self.msg_entry['state'] == tk.DISABLED: return
        
        msg = self.msg_entry.get()
        if msg and self.node.connection:
            if self.node.send_message(msg):
                self.log_message(f"Me: {msg}")
                self.msg_entry.delete(0, tk.END)
            else:
                self.log_message("Failed to send message.")

    def reset_buttons(self):
        self.host_btn.config(state=tk.NORMAL)
        self.connect_btn.config(state=tk.NORMAL)
        self.msg_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)

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
