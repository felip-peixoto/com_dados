import socket
import json

def enviar_sinal(host, porta, sinal_hdb3):
    """
    Serializa e envia lista de voltagens via socket.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, porta))
            dados = json.dumps(sinal_hdb3)
            s.sendall(dados.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Erro ao enviar: {e}")
        return False


def receber_sinal(porta, timeout=30):
    """
    Aguarda conexão e recebe sinal HDB3.
    Retorna lista de voltagens ou None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', porta))
            s.listen(1)
            s.settimeout(timeout)
            conn, addr = s.accept()
            with conn:
                dados = conn.recv(65536).decode('utf-8')
                return json.loads(dados)
    except socket.timeout:
        print("Timeout aguardando conexão.")
        return None
    except Exception as e:
        print(f"Erro ao receber: {e}")
        return None