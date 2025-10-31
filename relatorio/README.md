# Projeto Heatmap de Sinal Wi-Fi

Este script Python gera um mapa de calor (heatmap) interpolado da intensidade do sinal Wi-Fi a partir de medições de coordenadas (X, Y) e potência de sinal (dB).

## Como Rodar o Projeto 

1.  **Crie um Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    ```

2.  **Ative o Ambiente:**
    ```bash
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Atualize os Dados:**
    Abra o arquivo `dados_medicoes.csv` e insira suas medições de campo.

5.  **Execute o Script:**
    ```bash
    python gerar_heatmap.py
    ```
