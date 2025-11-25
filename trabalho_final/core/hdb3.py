def encode_hdb3(binary_string):
    """
    Codifica string binária em HDB3.
    Retorna lista de voltagens: [+1, 0, -1, ...]
    """
    binary_string = binary_string.replace(" ", "")
    signal = []
    last_polarity = 1  # começa positivo
    pulsos_desde_substituicao = 0
    
    i = 0
    while i < len(binary_string):
        # Detecta 4 zeros consecutivos
        if i <= len(binary_string) - 4 and binary_string[i:i+4] == "0000":
            if pulsos_desde_substituicao % 2 == 1:  # ímpar
                # 000V (V tem o mesmo sinal do último pulso válido)
                signal.extend([0, 0, 0, last_polarity])
                pulsos_desde_substituicao = 0 
            else:  # par
                # B00V (B inverte, V copia B)
                last_polarity = -last_polarity
                signal.append(last_polarity) # B
                signal.extend([0, 0, last_polarity]) # 00V
                pulsos_desde_substituicao = 0
            
            i += 4
        else:
            bit = binary_string[i]
            if bit == '1':
                last_polarity = -last_polarity
                signal.append(last_polarity)
                pulsos_desde_substituicao += 1
            else:
                signal.append(0)
            i += 1
    
    return signal


def decode_hdb3(signal):
    """
    Decodifica sinal HDB3 para string binária.
    Versão corrigida para evitar erros de polaridade acumulada.
    """
    binary = []
    i = 0
    last_pulse_polarity = 1  # Assume estado inicial padrão (positivo)
    
    while i < len(signal):
        # Tenta detectar B00V ou 000V (sequências de 4 pulsos)
        if i <= len(signal) - 4:
            # Padrão de violação (o 4º elemento é a violação V)
            # Verifica se signal[i+3] é diferente de 0 (é um pulso)
            if signal[i+1] == 0 and signal[i+2] == 0 and signal[i+3] != 0:
                # Aqui simplificamos: se achou X00V, assume que é HDB3 substitution
                # E converte os 4 slots para '0000'
                binary.extend(['0', '0', '0', '0'])
                # Atualiza a polaridade baseada na violação recebida para manter sincronia
                last_pulse_polarity = signal[i+3] 
                i += 4
                continue
        
        # Bit normal
        val = signal[i]
        if val == 0:
            binary.append('0')
        else:
            binary.append('1')
            last_pulse_polarity = val
            
        i += 1
    
    return ''.join(binary)