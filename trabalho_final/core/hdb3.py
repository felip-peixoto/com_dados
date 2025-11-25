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
            if signal[i+1] == 0 and signal[i+2] == 0 and signal[i+3] != 0:
                # Se for B00V ou 000V, são 4 zeros originais
                binary.extend(['0', '0', '0', '0'])
                # Atualiza a polaridade baseada na violação recebida
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