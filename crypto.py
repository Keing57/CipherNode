import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_key_pair():
    """Generates a 2048-bit RSA private and public key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    """Serializes public key to PEM format to send over the network."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(pem_bytes):
    """Deserializes PEM formatted public key."""
    return serialization.load_pem_public_key(pem_bytes)

def generate_aes_key():
    """Generates a 256-bit (32 bytes) AES symmetric key."""
    return os.urandom(32)
