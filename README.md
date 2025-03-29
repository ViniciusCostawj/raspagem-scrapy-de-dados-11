# Raspagem de Dados do Portal da Transparência

Este projeto realiza a raspagem de dados do site do Portal da Transparência, extraindo informações sobre servidores públicos e salvando os resultados em arquivos `.txt` e `.json`.

## 📌 Funcionalidades

- Acessa o site do Portal da Transparência.
- Aceita os cookies automaticamente.
- Localiza a tabela de servidores públicos.
- Extrai dados relevantes, como nome, CPF, órgão de lotação, cargo, etc.
- Salva os dados extraídos em arquivos `resultado.txt` e `resultado.json`.

## 🚀 Como Executar

### 1️⃣ Instale as dependências
Antes de rodar o script, certifique-se de ter o Python e as dependências instaladas:

```sh
pip install selenium webdriver-manager
