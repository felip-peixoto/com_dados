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
                # 000V
                signal.extend([0, 0, 0, last_polarity])
            else:  # par
                # B00V
                last_polarity = -last_polarity
                signal.append(last_polarity)
                signal.extend([0, 0, last_polarity])
            
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
    """
    binary = []
    i = 0
    
    while i < len(signal):
        # Detecta padrão 000V ou B00V
        if i <= len(signal) - 4:
            # Verifica 000V (3 zeros + violação)
            if signal[i:i+3] == [0, 0, 0] and signal[i+3] != 0:
                binary.extend(['0', '0', '0', '0'])
                i += 4
                continue
            # Verifica B00V (pulso + 2 zeros + violação)
            elif signal[i] != 0 and signal[i+1:i+3] == [0, 0] and signal[i+3] != 0:
                binary.extend(['0', '0', '0', '0'])
                i += 4
                continue
        
        # Bit normal
        if signal[i] == 0:
            binary.append('0')
        else:
            binary.append('1')
        i += 1
    
    return ''.join(binary)