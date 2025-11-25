def encode_hdb3(binary_string):
    """
    Codifica string binária em HDB3.
    Retorna lista de voltagens: [+1, 0, -1, ...]
    """
    binary_string = binary_string.replace(" ", "")
    signal = []
    last_polarity = 1  # começa positivo (então o primeiro 1 vira -1)
    pulsos_desde_substituicao = 0
    
    i = 0
    while i < len(binary_string):
        # Detecta 4 zeros consecutivos
        if i <= len(binary_string) - 4 and binary_string[i:i+4] == "0000":
            if pulsos_desde_substituicao % 2 == 1:  # ímpar
                # 000V (V tem o mesmo sinal do último pulso válido)
                signal.extend([0, 0, 0, last_polarity])
                # Nota: V conta como pulso para fins de polaridade? 
                # No HDB3, o bit de violação carrega a polaridade.
                # Atualizamos o 'pulso' para manter a regra de violação
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
    Corrige o bug de identificar falsos positivos de violação.
    """
    binary = []
    i = 0
    last_pulse_polarity = 1 # Assume estado inicial igual ao encoder
    
    while i < len(signal):
        # 1. Tenta detectar B00V: Padrão [+/-1, 0, 0, +/-1]
        # Para ser B00V, o primeiro e o quarto elemento devem ter o MESMO sinal.
        if i <= len(signal) - 4:
            if signal[i] != 0 and signal[i+1] == 0 and signal[i+2] == 0 and signal[i+3] != 0:
                if signal[i] == signal[i+3]: # Violação de polaridade detectada (B == V)
                    binary.extend(['0', '0', '0', '0'])
                    last_pulse_polarity = signal[i+3]
                    i += 4
                    continue
        
        # 2. Tenta detectar 000V: Padrão [0, 0, 0, +/-1]
        # Para ser 000V, o quarto elemento deve ter o MESMO sinal do último pulso histórico.
        if i <= len(signal) - 4:
             if signal[i] == 0 and signal[i+1] == 0 and signal[i+2] == 0 and signal[i+3] != 0:
                if signal[i+3] == last_pulse_polarity: # Violação (V == último pulso)
                    binary.extend(['0', '0', '0', '0'])
                    last_pulse_polarity = signal[i+3]
                    i += 4
                    continue
        
        # 3. Bit normal
        val = signal[i]
        if val == 0:
            binary.append('0')
        else:
            binary.append('1')
            last_pulse_polarity = val # Atualiza referência de polaridade
            
        i += 1
    
    return ''.join(binary)