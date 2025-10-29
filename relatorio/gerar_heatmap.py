import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

ARQUIVO_DADOS = 'dados_medicoes.csv'
ARQUIVO_PORTAS = 'portas_corredor.csv'
COLUNAS_PARA_MAPEAR = ['UTFPR-SERVIDOR', 'UTFPR-VISITANTE', 'UTFPR-ALUNO']
SIGMA_SUAVIZACAO = 15 #Blur do mapa de relevo

VALOR_PONTO_MORTO = -100

DPI_SAIDA = 300 

VMIN_GLOBAL = -100
VMAX_GLOBAL = -35

EXTENSAO_PORTA_PADRAO = 0.81
EXTENSAO_PORTA_EXCECAO = 0.405
PORTAS_EXCECAO = ['CQ211', 'Banheiro'] 

LARGURA_LINHA_CORREDOR = 3
COR_LINHA_CORREDOR = 'black' 

LARGURA_LINHA_PORTA = 4
COR_LINHA_PORTA = 'red'
# -------------------------------------

def limpar_dados_db(df, colunas_db, dead_spot_value):
    for col in colunas_db:
        if col in df.columns:
            # Garante que 'XXX' ou outros não-numéricos virem NaN antes de preencher
            df[col] = pd.to_numeric(df[col], errors='coerce') 
            df[col] = df[col].fillna(dead_spot_value)
    return df

def draw_corridor_and_doors(ax, df_portas, x_min_plot, x_max_plot, y_parede_inf, y_parede_sup):
    """
    Desenha o retângulo do corredor (preto) e as portas (vermelho) com nomes.
    """
    
    ax.plot([x_min_plot, x_max_plot], [y_parede_inf, y_parede_inf], color=COR_LINHA_CORREDOR, linewidth=LARGURA_LINHA_CORREDOR, zorder=3)
    ax.plot([x_min_plot, x_max_plot], [y_parede_sup, y_parede_sup], color=COR_LINHA_CORREDOR, linewidth=LARGURA_LINHA_CORREDOR, zorder=3)
    ax.plot([x_min_plot, x_min_plot], [y_parede_inf, y_parede_sup], color=COR_LINHA_CORREDOR, linewidth=LARGURA_LINHA_CORREDOR, zorder=3)
    ax.plot([x_max_plot, x_max_plot], [y_parede_inf, y_parede_sup], color=COR_LINHA_CORREDOR, linewidth=LARGURA_LINHA_CORREDOR, zorder=3)
    
    for index, row in df_portas.iterrows():
        lugar = row['LUGAR']
        x_centro = row['X_CENTRO']
        y_posicao = row['Y_POSICAO']

        extensao = EXTENSAO_PORTA_EXCECAO if lugar in PORTAS_EXCECAO else EXTENSAO_PORTA_PADRAO
        
        x_inicio_porta = x_centro - extensao
        x_fim_porta = x_centro + extensao
        
        if np.isclose(y_posicao, y_parede_inf):
            ax.plot([x_inicio_porta, x_fim_porta], [y_parede_inf, y_parede_inf], color=COR_LINHA_PORTA, linewidth=LARGURA_LINHA_PORTA, zorder=4)
            ax.text(x_centro, y_parede_inf + 0.05, lugar, # 0.05 é um pequeno offset acima da porta
                    color='white', fontsize=8, ha='center', va='bottom', zorder=5,
                    bbox=dict(facecolor='black', alpha=0.5, pad=0.1, edgecolor='none')) # Adiciona fundo semi-transparente
        elif np.isclose(y_posicao, y_parede_sup):
            ax.plot([x_inicio_porta, x_fim_porta], [y_parede_sup, y_parede_sup], color=COR_LINHA_PORTA, linewidth=LARGURA_LINHA_PORTA, zorder=4)
            ax.text(x_centro, y_parede_sup - 0.05, lugar, # 0.05 é um pequeno offset abaixo da porta
                    color='white', fontsize=8, ha='center', va='top', zorder=5,
                     bbox=dict(facecolor='black', alpha=0.5, pad=0.1, edgecolor='none')) # Adiciona fundo semi-transparente


def generate_heatmap(df, df_portas, column_name, output_filename, 
                     x_min_plot, x_max_plot, y_min_plot, y_max_plot, 
                     y_parede_inf, y_parede_sup, vmin, vmax): 
    
    print(f"\n--- Iniciando geração do mapa para: {column_name} ---")
    
    df_clean = df.dropna(subset=['X', 'Y', column_name])
    
    if df_clean.empty:
        print(f"Erro: Não há dados válidos (com X, Y) para plotar para {column_name}.")
        return 

    print(f"Dados processados. {len(df_clean)} pontos válidos para '{column_name}'.")

    x = df_clean['X'].values
    y = df_clean['Y'].values
    z = df_clean[column_name].values

    grid_x, grid_y = np.mgrid[x_min_plot:x_max_plot:500j, y_min_plot:y_max_plot:500j]

    print("Interpolando dados (Linear + Vizinho Próximo)...")
    grid_z_linear = griddata((x, y), z, (grid_x, grid_y), method='linear')
    grid_z_nearest = griddata((x, y), z, (grid_x, grid_y), method='nearest')
    grid_z_linear[np.isnan(grid_z_linear)] = grid_z_nearest[np.isnan(grid_z_linear)]
    
    print(f"Suavizando o mapa (Sigma={SIGMA_SUAVIZACAO})...")
    grid_z_suave = gaussian_filter(grid_z_linear, sigma=SIGMA_SUAVIZACAO)
    
    print("Gerando o gráfico...")
    plt.figure(figsize=(13, 7))
    ax = plt.gca()
    
    im = ax.imshow(grid_z_suave.T, origin='lower', 
                    extent=[x_min_plot, x_max_plot, y_min_plot, y_max_plot], 
                    cmap='viridis', aspect='auto', zorder=1,
                    vmin=vmin, vmax=vmax) 
    
    ax.grid(True, linestyle=':', alpha=0.3, color='white', zorder=2)
    
    draw_corridor_and_doors(ax, df_portas, x_min_plot, x_max_plot, y_parede_inf, y_parede_sup)
    
    ax.scatter(x, y, c='red', s=20, edgecolor='black', label='Pontos de Medição', zorder=6, linewidth=0.8)
    
    plt.colorbar(im, label=f'Intensidade (dBm) - {column_name}') # Mudei para dBm
    plt.xlabel('Coordenada X (metros)')
    plt.ylabel('Coordenada Y (metros)')
    plt.title(f'Rede {column_name}')
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=False, shadow=False, ncol=1, frameon=False)
    
    plt.xlim(x_min_plot, x_max_plot)
    plt.ylim(y_min_plot, y_max_plot)
    
    plt.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.2)

    nome_arquivo_final = f"heatmap_{column_name.lower().replace('-', '_')}.png" # Nome seguro para arquivo
    
    plt.savefig(nome_arquivo_final, dpi=DPI_SAIDA)
    
    plt.close() 
    print(f"Sucesso! Mapa salvo como '{nome_arquivo_final}' (Escala Fixa: {vmin} a {vmax} dBm, {DPI_SAIDA} DPI)")

def main():
    print(f"Iniciando processo...")
    
    try:
        df_medicoes = pd.read_csv(ARQUIVO_DADOS, sep=';', decimal='.')
        print(f"Carregados dados de medição de '{ARQUIVO_DADOS}'")
        df_portas = pd.read_csv(ARQUIVO_PORTAS, sep=';', decimal='.')
        print(f"Carregados dados das portas de '{ARQUIVO_PORTAS}'")
        
    except FileNotFoundError as e:
        print(f"Erro Crítico: Arquivo não encontrado.")
        print(f"Detalhe: {e}")
        return
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return

    MARGEM_X = 0.0 # Sem folga lateral
    MARGEM_Y = 0.0 # Sem folga vertical

    if 'X' in df_medicoes.columns and not df_medicoes['X'].empty:
        X_MIN_PLOT = df_medicoes['X'].min() - MARGEM_X
        X_MAX_PLOT = df_medicoes['X'].max() + MARGEM_X
    else:
        print("Erro: Coluna 'X' não encontrada ou vazia no CSV de medições.")
        return
        
    if 'Y' in df_medicoes.columns and not df_medicoes['Y'].empty:
        Y_MIN_PLOT = df_medicoes['Y'].min() - MARGEM_Y
        Y_MAX_PLOT = df_medicoes['Y'].max() + MARGEM_Y
        Y_PAREDE_INFERIOR = df_medicoes['Y'].min() # Coordenada exata da parede
        Y_PAREDE_SUPERIOR = df_medicoes['Y'].max() # Coordenada exata da parede
    else:
        print("Erro: Coluna 'Y' não encontrada ou vazia no CSV de medições.")
        return

    print(f"Limites do plot definidos: X({X_MIN_PLOT:.2f} a {X_MAX_PLOT:.2f}), Y({Y_MIN_PLOT:.2f} a {Y_MAX_PLOT:.2f})")
    print(f"Paredes do corredor em Y={Y_PAREDE_INFERIOR} e Y={Y_PAREDE_SUPERIOR}")

    df_processed = limpar_dados_db(df_medicoes.copy(), COLUNAS_PARA_MAPEAR, VALOR_PONTO_MORTO)
    
    for coluna in COLUNAS_PARA_MAPEAR:
        if coluna in df_processed.columns:
            generate_heatmap(df_processed, df_portas, coluna, 
                             f"heatmap_{coluna.lower().replace('-', '_')}.png", 
                             X_MIN_PLOT, X_MAX_PLOT, Y_MIN_PLOT, Y_MAX_PLOT,
                             Y_PAREDE_INFERIOR, Y_PAREDE_SUPERIOR,
                             VMIN_GLOBAL, VMAX_GLOBAL) 
        else:
            print(f"\nAviso: Coluna '{coluna}' não encontrada no CSV de medições. Pulando...")
            
    print("\nProcesso finalizado. Todos os mapas foram gerados.")

if __name__ == "__main__":
    main()