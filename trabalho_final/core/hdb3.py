def decode_hdb3(signal):
    """
    Decodifica sinal HDB3 para string binária.
    Retorna TUPLA: (string_binaria, string_simbolica)
    Ex: ("0000", "B 0 0 V")
    """
    binary = []
    simbolos = [] # Nova lista para guardar os símbolos
    i = 0
    last_pulse_polarity = 1
    
    while i < len(signal):
        decoded = False
        
        # 1. Tenta detectar B00V
        if i <= len(signal) - 4:
            val_b = signal[i]
            val_01 = signal[i+1]
            val_02 = signal[i+2]
            val_v = signal[i+3]
            
            if val_b != 0 and val_01 == 0 and val_02 == 0 and val_v != 0:
                if val_b == val_v: # Polaridades iguais = Violação com B
                    binary.extend(['0', '0', '0', '0'])
                    simbolos.extend(['B', '0', '0', 'V']) # Registra visualmente
                    
                    last_pulse_polarity = val_v
                    i += 4
                    decoded = True
                    continue

        # 2. Tenta detectar 000V
        if not decoded and i <= len(signal) - 4:
            val_01 = signal[i]
            val_02 = signal[i+1]
            val_03 = signal[i+2]
            val_v = signal[i+3]
            
            if val_01 == 0 and val_02 == 0 and val_03 == 0 and val_v != 0:
                if val_v == last_pulse_polarity: # Polaridade igual ao anterior = Violação
                    binary.extend(['0', '0', '0', '0'])
                    simbolos.extend(['0', '0', '0', 'V']) # Registra visualmente
                    
                    last_pulse_polarity = val_v
                    i += 4
                    decoded = True
                    continue
        
        # 3. Bit Normal
        if not decoded:
            val = signal[i]
            if val == 0:
                binary.append('0')
                simbolos.append('0')
            else:
                binary.append('1')
                simbolos.append('1')
                last_pulse_polarity = val
            i += 1
    
    return ''.join(binary), " ".join(simbolos)