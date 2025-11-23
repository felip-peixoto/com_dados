def cifrar_vigenere(texto, chave):
    """
    Cifra usando Vigenère com ASCII estendido (0-255).
    """
    if not chave:
        return None
    
    chave_bytes = chave.encode('latin-1')
    texto_bytes = texto.encode('latin-1')
    
    cifrado = []
    for i, byte in enumerate(texto_bytes):
        chave_byte = chave_bytes[i % len(chave_bytes)]
        cifrado.append((byte + chave_byte) % 256)
    
    return bytes(cifrado).decode('latin-1')


def decifrar_vigenere(texto_cifrado, chave):
    """
    Decifra Vigenère.
    """
    if not chave:
        return None
    
    chave_bytes = chave.encode('latin-1')
    cifrado_bytes = texto_cifrado.encode('latin-1')
    
    decifrado = []
    for i, byte in enumerate(cifrado_bytes):
        chave_byte = chave_bytes[i % len(chave_bytes)]
        decifrado.append((byte - chave_byte) % 256)
    
    return bytes(decifrado).decode('latin-1')