# 🎵 Billboard Top Songs com Spotify

Aplicação web que mostra as músicas mais ouvidas nos EUA (Top da Billboard) em uma época específica, com links diretos para ouvir no Spotify.

## 🚀 Funcionalidades

- Consulta o Top 100 da Billboard por mês/ano
- Exibe informações detalhadas de cada música
- Links diretos para ouvir no Spotify
- Interface intuitiva com Streamlit

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Spotify Developer (para API credentials)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/lazarorx/billboard-spotify-app.git
cd billboard-spotify-app
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as credenciais do Spotify:
   - Acesse https://developer.spotify.com/dashboard
   - Crie um novo app
   - Copie o Client ID e Client Secret
   - Crie um arquivo `.env` baseado no `.env.example`
   - Cole suas credenciais no arquivo `.env`

## ▶️ Como usar

Execute a aplicação:
```bash
streamlit run app.py
```

A aplicação abrirá no navegador em `http://localhost:8501`

## 🛠️ Tecnologias

- **Streamlit**: Interface web
- **billboard.py**: API da Billboard
- **Spotipy**: API do Spotify
- **Pandas**: Manipulação de dados

## 👤 Autor

**lazarorx**

## 📝 Licença

MIT License
