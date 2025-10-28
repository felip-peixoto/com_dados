import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

# --- Configurações ---
ARQUIVO_DADOS = 'dados_medicoes.csv'
COLUNAS_PARA_MAPEAR = ['DBSERVIDOR', 'DBVISITANTE', 'DBALUNO']
SIGMA_SUAVIZACAO = 15 # Intensidade do "blur" (mapa de relevo)

# --- [ IMPORTANTE ] CONFIGURAÇÕES DO MAPA ---
# Ajustado para o novo layout de corredor 30x10 (X > Y)
X_MIN = 0.0   # Início do corredor
X_MAX = 30.0  # Fim do corredor (comprido)
Y_MIN = 0.0   # Parede de baixo
Y_MAX = 10.0  # Parede de cima (estreito)
# -------------------------------------

def limpar_dados_db(df, colunas_db):
    """Converte colunas de $dB$ para numérico, tratando 'XXX' e outros erros."""
    for col in colunas_db:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def generate_heatmap(df, column_name, output_filename, x_min, x_max, y_min, y_max):
    """
    Gera e salva um mapa de calor suave para uma coluna de $dB$ específica.
    """
    print(f"\n--- Iniciando geração do mapa para: {column_name} ---")
    
    # 1. Limpar dados específicos
    df_clean = df.dropna(subset=['X', 'Y', column_name])
    
    if df_clean.empty:
        print(f"Erro: Não há dados válidos (com X, Y e {column_name}) para plotar.")
        return 

    print(f"Dados processados. {len(df_clean)} pontos válidos para '{column_name}'.")

    # 2. Preparar pontos
    x = df_clean['X'].values
    y = df_clean['Y'].values
    z = df_clean[column_name].values

    # 3. Criar grade (Alta resolução)
    grid_x, grid_y = np.mgrid[x_min:x_max:500j, y_min:y_max:500j]

    # 4. Interpolar (Linear)
    print("Interpolando dados (Método Linear)...")
    grid_z_linear = griddata((x, y), z, (grid_x, grid_y), method='linear')

    # 5. Interpolar (Preencher cantos)
    print("Interpolando dados (Método Vizinho Próximo)...")
    grid_z_nearest = griddata((x, y), z, (grid_x, grid_y), method='nearest')
    
    # 6. Combinar
    grid_z_linear[np.isnan(grid_z_linear)] = grid_z_nearest[np.isnan(grid_z_linear)]
    
    # 7. Suavizar (O "mapa de relevo")
    print(f"Suavizando o mapa (Sigma={SIGMA_SUAVIZACAO})...")
    grid_z_suave = gaussian_filter(grid_z_linear, sigma=SIGMA_SUAVIZACAO)
    
    # 8. Plotar e Salvar
    print("Gerando o gráfico...")
    # Ajustei o figsize para ficar mais comprido (largura 13, altura 7)
    plt.figure(figsize=(13, 7))
    
    im = plt.imshow(grid_z_suave.T, origin='lower', 
                    extent=[x_min, x_max, y_min, y_max], 
                    cmap='viridis', aspect='auto')
    
    plt.scatter(x, y, c='red', s=15, edgecolor='black', label='Pontos de Medição')
    
    plt.colorbar(im, label=f'Intensidade (dB) - {column_name}')
    plt.xlabel('Coordenada X (metros)')
    plt.ylabel('Coordenada Y (metros)')
    plt.title(f'Mapa de Calor Suave - Rede {column_name}')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.3, color='white')
    
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.tight_layout()

    plt.savefig(output_filename)
    plt.close() 
    print(f"Sucesso! Mapa salvo como '{output_filename}'")

def main():
    print(f"Iniciando processo... Carregando dados de '{ARQUIVO_DADOS}'")
    
    try:
        df = pd.read_csv(ARQUIVO_DADOS, sep=';', decimal='.')
    except FileNotFoundError:
        print(f"Erro: Arquivo '{ARQUIVO_DADOS}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return

    df = limpar_dados_db(df, COLUNAS_PARA_MAPEAR)
    
    for coluna in COLUNAS_PARA_MAPEAR:
        if coluna in df.columns:
            nome_arquivo = f"heatmap_{coluna.lower()}.png"
            generate_heatmap(df, coluna, nome_arquivo, 
                             X_MIN, X_MAX, Y_MIN, Y_MAX)
        else:
            print(f"\nAviso: Coluna '{coluna}' não encontrada no CSV. Pulando...")
            
    print("\nProcesso finalizado. Todos os mapas foram gerados.")

if __name__ == "__main__":
    main()