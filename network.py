import socket
import threading

class P2PNode:
    def __init__(self, on_connected=None, on_disconnected=None, on_message=None, on_error=None):
        self.server_socket = None
        self.connection = None
        self.address = None
        self.receive_thread = None
        self.running = False
        
        # Callbacks
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.on_message = on_message
        self.on_error = on_error

    def start_hosting(self, host, port):
        def host_thread():
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((host, port))
                self.server_socket.listen(1)
                
                self.connection, self.address = self.server_socket.accept()
                if self.on_connected:
                    self.on_connected()
                
                self.start_receiving()
            except Exception as e:
                if self.on_error:
                    self.on_error(str(e))
                print(f"Hosting error: {e}")

        threading.Thread(target=host_thread, daemon=True).start()

    def connect_to_host(self, host, port):
        def connect_thread():
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((host, port))
                self.address = (host, port)
                if self.on_connected:
                    self.on_connected()
                
                self.start_receiving()
            except Exception as e:
                if self.on_error:
                    self.on_error(str(e))
                print(f"Connection error: {e}")

        threading.Thread(target=connect_thread, daemon=True).start()

    def start_receiving(self):
        self.running = True
        def receive_loop():
            while self.running:
                try:
                    data = self.connection.recv(1024)
                    if not data:
                        break
                    if self.on_message:
                        self.on_message(data.decode('utf-8'))
                except ConnectionResetError:
                    print("Connection reset by peer.")
                    break
                except Exception as e:
                    print(f"Receive error: {e}")
                    break
            
            self.running = False
            self.close_connection()
            if self.on_disconnected:
                self.on_disconnected()

        self.receive_thread = threading.Thread(target=receive_loop, daemon=True)
        self.receive_thread.start()

    def send_message(self, message):
        if self.connection and self.running:
            try:
                self.connection.sendall(message.encode('utf-8'))
                return True
            except ConnectionResetError:
                print("Send error: Connection reset by peer.")
                self.running = False
                self.close_connection()
            except Exception as e:
                print(f"Send error: {e}")
                self.running = False
                self.close_connection()
        return False

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
        self.running = False
