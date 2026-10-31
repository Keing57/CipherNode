import socket
import threading

class P2PNode:
    def __init__(self):
        self.server_socket = None
        self.connection = None
        self.address = None

    def start_hosting(self, host, port, on_connected_callback=None, on_error_callback=None):
        def host_thread():
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((host, port))
                self.server_socket.listen(1)
                
                self.connection, self.address = self.server_socket.accept()
                if on_connected_callback:
                    on_connected_callback()
            except Exception as e:
                if on_error_callback:
                    on_error_callback(str(e))
                print(f"Hosting error: {e}")

        threading.Thread(target=host_thread, daemon=True).start()

    def connect_to_host(self, host, port, on_connected_callback=None, on_error_callback=None):
        def connect_thread():
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((host, port))
                self.address = (host, port)
                if on_connected_callback:
                    on_connected_callback()
            except Exception as e:
                if on_error_callback:
                    on_error_callback(str(e))
                print(f"Connection error: {e}")

        threading.Thread(target=connect_thread, daemon=True).start()
