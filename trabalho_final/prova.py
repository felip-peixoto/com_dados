import matplotlib.pyplot as plt
from core.hdb3 import encode_hdb3

def teste_hdb3():
    binario = "1100001000000000"
    
    sinal = encode_hdb3(binario)
    
    plt.figure(figsize=(12, 5))
    
    plt.step(range(len(sinal)), sinal, where='post', linewidth=3, color='blue')
    
    plt.title(f"Teste HDB3\nBinário: {binario}", fontsize=14)
    plt.xlabel("Tempo")
    plt.ylabel("Tensão")
    plt.ylim(-1.5, 1.5)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.axhline(0, color='black', linewidth=1)
    
    for i, bit in enumerate(binario):
        plt.text(i + 0.5, 1.2, bit, ha='center', fontweight='bold')

    plt.savefig("teste.png")

if __name__ == "__main__":
    try:
        teste_hdb3()
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")