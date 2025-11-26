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
    Aguarda conexão e recebe sinal HDB3 (COM LOOP DE BUFFER).
    Retorna lista de voltagens ou None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', porta))
            s.listen(1)
            s.settimeout(timeout)
            print(f"Aguardando conexão na porta {porta}...")
            conn, addr = s.accept()
            with conn:
                print(f"Conectado por {addr}")
                
                # --- SOLUÇÃO PARA TEXTÃO: LER EM LOOP ---
                dados_completos = b""
                while True:
                    # Lê pedaços de 4096 bytes
                    parte = conn.recv(4096)
                    if not parte:
                        break # Fim da transmissão
                    dados_completos += parte
                
                # Decodifica só no final
                dados_str = dados_completos.decode('utf-8')
                return json.loads(dados_str)

    except socket.timeout:
        print("Timeout aguardando conexão.")
        return None
    except Exception as e:
        print(f"Erro ao receber: {e}")
        return None