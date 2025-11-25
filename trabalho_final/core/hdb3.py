def encode_hdb3(binary_string):
    """
    Codifica string binária em HDB3.
    Retorna lista de voltagens: [+1, 0, -1, ...]
    """
    binary_string = binary_string.replace(" ", "")
    signal = []
    last_polarity = -1  # começa positivo
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
    Versão corrigida: verifica ESTRITAMENTE a polaridade para não confundir dados com violação.
    """
    binary = []
    i = 0
    last_pulse_polarity = 1  # Estado inicial deve bater com o encoder (positivo)
    
    while i < len(signal):
        decoded = False
        
        # 1. Tenta detectar B00V (Padrão: Pulso, 0, 0, Pulso)
        # Regra: O primeiro e o último pulso devem ter o MESMO sinal (Violação)
        if i <= len(signal) - 4:
            val_b = signal[i]
            val_01 = signal[i+1]
            val_02 = signal[i+2]
            val_v = signal[i+3]
            
            if val_b != 0 and val_01 == 0 and val_02 == 0 and val_v != 0:
                if val_b == val_v: # AQUI ESTÁ A CORREÇÃO: Checa polaridade
                    # Achou B00V -> Substitui por 0000
                    binary.extend(['0', '0', '0', '0'])
                    last_pulse_polarity = val_v # Atualiza polaridade
                    i += 4
                    decoded = True
                    continue

        # 2. Tenta detectar 000V (Padrão: 0, 0, 0, Pulso)
        # Regra: O pulso V deve ter o MESMO sinal do último pulso histórico
        if not decoded and i <= len(signal) - 4:
            val_01 = signal[i]
            val_02 = signal[i+1]
            val_03 = signal[i+2]
            val_v = signal[i+3]
            
            if val_01 == 0 and val_02 == 0 and val_03 == 0 and val_v != 0:
                if val_v == last_pulse_polarity: # AQUI ESTÁ A CORREÇÃO: Checa polaridade
                    # Achou 000V -> Substitui por 0000
                    binary.extend(['0', '0', '0', '0'])
                    last_pulse_polarity = val_v # Atualiza polaridade
                    i += 4
                    decoded = True
                    continue
        
        # 3. Bit Normal
        if not decoded:
            val = signal[i]
            if val == 0:
                binary.append('0')
            else:
                binary.append('1')
                last_pulse_polarity = val
            i += 1
    
    return ''.join(binary)