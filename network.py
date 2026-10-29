import socket
import threading

class P2PNode:
    def __init__(self):
        self.server_socket = None
        self.connection = None
        self.address = None

    def start_hosting(self, host, port, on_connected_callback=None):
        def host_thread():
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((host, port))
                self.server_socket.listen(1)
                
                self.connection, self.address = self.server_socket.accept()
                if on_connected_callback:
                    on_connected_callback()
            except Exception as e:
                print(f"Hosting error: {e}")

        threading.Thread(target=host_thread, daemon=True).start()
