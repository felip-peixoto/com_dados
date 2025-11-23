def texto_para_binario(texto):
    try:
        bytes_texto = texto.encode('latin-1') #Tabela Ascii Estendida
        lista_binaria = []
        for byte in bytes_texto:
            lista_binaria.append(f'{byte:08b}') #Converte para binario (b), com 8 digitos de largura (8, "em bytes") e preenche com zeros a esqueda quando não deu 8 bits (0)
        return "".join(lista_binaria)
    except UnicodeEncodeError:
        print("ERRO: CARACETERES INVÁLIDOS ENCONTRADOS!")
        return None

def binario_para_texto(binario_str):
    binario_str = binario_str.replace(" ", "") #Remove espaços em branco

    if len(binario_str) % 8 != 0:
        print(f"ERRO: TAMANHO INVÁLIDO! DEVE SER MULTIPLO DE 8, TAMANHO ENCONTRADO: ({len(binario_str)} BITS)")
        return None
    try:
        lista_chars = []
        for i in range(0, len(binario_str), 8):
            byte_str = binario_str[i : i+8]
            decimal = int(byte_str, 2)
            lista_chars.append(chr(decimal))
        return "".join(lista_chars)
    except ValueError:
        print("ERRO: CARACETERES INVÁLIDOS ENCONTRADOS!")
        return None

if __name__ == "__main__":
    print("Escolha o modo: ")
    print("[1] Texto   -> Binário")
    print("[0] Binário -> Texto")
    
    escolha = input("Escolhido: ").strip()

    if escolha == '1':
        entrada = input("\nTexto: ")
        resultado = texto_para_binario(entrada)
        if resultado:
            print(f"\nBinário: {resultado}")

    elif escolha == '0':
        entrada = input("\nBinário: ")
        resultado = binario_para_texto(entrada)
        if resultado:
            print(f"\nTexto: {resultado}")
            
    else:
        print("Opção inválida. Digite apenas 1 ou 0.")