import tkinter as tk
from tkinter import scrolledtext

def main():
    root = tk.Tk()
    root.title("P2P Chat")
    root.geometry("600x500")

    # Top Frame for Connection
    top_frame = tk.Frame(root)
    top_frame.pack(padx=10, pady=10, fill=tk.X)

    tk.Label(top_frame, text="IP:").pack(side=tk.LEFT)
    ip_entry = tk.Entry(top_frame, width=15)
    ip_entry.pack(side=tk.LEFT, padx=(0, 10))

    tk.Label(top_frame, text="Port:").pack(side=tk.LEFT)
    port_entry = tk.Entry(top_frame, width=8)
    port_entry.pack(side=tk.LEFT, padx=(0, 10))

    connect_btn = tk.Button(top_frame, text="Connect")
    connect_btn.pack(side=tk.LEFT, padx=(0, 5))

    host_btn = tk.Button(top_frame, text="Host")
    host_btn.pack(side=tk.LEFT)

    # Middle Frame for Chat
    chat_frame = tk.Frame(root)
    chat_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

    chat_text = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED)
    chat_text.pack(fill=tk.BOTH, expand=True)

    # Bottom Frame for Input
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

    msg_entry = tk.Entry(bottom_frame)
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

    send_btn = tk.Button(bottom_frame, text="Send", width=10)
    send_btn.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()
