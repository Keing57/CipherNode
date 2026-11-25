import socket
import threading
from crypto import (
    generate_rsa_key_pair, serialize_public_key, deserialize_public_key,
    generate_aes_key, rsa_encrypt, rsa_decrypt, aes_encrypt, aes_decrypt
)

class P2PNode:
    def __init__(self, on_connected=None, on_disconnected=None, on_message=None, on_error=None):
        self.server_socket = None
        self.connection = None
        self.address = None
        self.receive_thread = None
        self.running = False
        self.is_host = False
        
        # Callbacks
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.on_message = on_message
        self.on_error = on_error
        
        # Crypto
        self.private_key, self.public_key = generate_rsa_key_pair()
        self.peer_public_key = None
        self.aes_key = None

    def _handshake(self):
        # Sequential handshake to establish keys securely
        if self.is_host:
            # 1. Receive client's public key
            client_pk_bytes = self.connection.recv(1024)
            self.peer_public_key = deserialize_public_key(client_pk_bytes)
            # 2. Send our public key
            self.connection.sendall(serialize_public_key(self.public_key))
            # 3. Receive encrypted AES key (256 bytes for RSA-2048)
            encrypted_aes = self.connection.recv(1024)
            self.aes_key = rsa_decrypt(self.private_key, encrypted_aes)
            print("Handshake complete (Host). AES key established.")
        else:
            # 1. Send our public key
            self.connection.sendall(serialize_public_key(self.public_key))
            # 2. Receive host's public key
            host_pk_bytes = self.connection.recv(1024)
            self.peer_public_key = deserialize_public_key(host_pk_bytes)
            # 3. Generate AES key, encrypt with host's PK, send
            self.aes_key = generate_aes_key()
            encrypted_aes = rsa_encrypt(self.peer_public_key, self.aes_key)
            self.connection.sendall(encrypted_aes)
            print("Handshake complete (Client). AES key established.")

    def start_hosting(self, host, port):
        self.is_host = True
        def host_thread():
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((host, port))
                self.server_socket.listen(1)
                
                self.connection, self.address = self.server_socket.accept()
                
                self._handshake()
                self.start_receiving()
                
                if self.on_connected:
                    self.on_connected()
            except Exception as e:
                if self.on_error:
                    self.on_error(str(e))
                print(f"Hosting error: {e}")

        threading.Thread(target=host_thread, daemon=True).start()

    def connect_to_host(self, host, port):
        self.is_host = False
        def connect_thread():
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((host, port))
                self.address = (host, port)
                
                self._handshake()
                self.start_receiving()
                
                if self.on_connected:
                    self.on_connected()
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
                    data = self.connection.recv(4096)
                    if not data:
                        break
                    
                    if self.on_message and self.aes_key:
                        try:
                            # Decrypt incoming message
                            plaintext = aes_decrypt(self.aes_key, data)
                            self.on_message(plaintext.decode('utf-8'))
                        except Exception as crypto_err:
                            print(f"Decryption error: {crypto_err}")
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
        if self.connection and self.running and self.aes_key:
            try:
                # Encrypt message before sending
                ciphertext = aes_encrypt(self.aes_key, message.encode('utf-8'))
                self.connection.sendall(ciphertext)
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
        self.peer_public_key = None
        self.aes_key = None
