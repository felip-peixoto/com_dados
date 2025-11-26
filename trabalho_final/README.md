# Implementacao de Codificacao de Linha - HDB3

Este projeto e uma implementacao do algoritmo HDB3 para a disciplina de Comunicacao de Dados. O programa permite enviar mensagens de texto de um computador para outro, mostrando o grafico da onda, o codigo binario e a criptografia.

## Funcionalidades

* Codificacao HDB3 com regras de violacao.
* Envio e recepcao de dados pela rede (entre dois computadores).
* Visualizacao grafica do sinal.
* Criptografia (Vigenere).

## Como instalar e preparar o ambiente

Como cada computador pode ter configuracoes diferentes, recomenda-se criar um ambiente virtual para rodar o projeto sem erros.

Siga os passos abaixo no terminal (Prompt de Comando ou PowerShell), dentro da pasta do projeto.

### Como rodar o projeto

**No Windows:**
python -m venv venv

.\venv\Scripts\activate

**No Linux ou Mac:**
python3 -m venv venv

source venv/bin/activate

**Em qualquer um**
pip install -r requirements.txt

python main.py
