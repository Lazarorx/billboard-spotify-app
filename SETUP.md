# 🚀 Setup Rápido

## 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

## 2️⃣ Configurar Spotify API

1. Acesse: https://developer.spotify.com/dashboard
2. Faça login com sua conta Spotify
3. Clique em "Create app"
4. Preencha:
   - App name: Billboard Spotify App
   - App description: App para buscar músicas da Billboard
   - Redirect URI: http://localhost:8501
5. Aceite os termos e clique em "Save"
6. Copie o **Client ID** e **Client Secret**

## 3️⃣ Criar arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```
SPOTIPY_CLIENT_ID=seu_client_id_aqui
SPOTIPY_CLIENT_SECRET=seu_client_secret_aqui
```

## 4️⃣ Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em: http://localhost:8501

## 🎯 Como Usar

1. No menu lateral, selecione o **ano** e **mês**
2. Clique em **Buscar Top Songs**
3. Aguarde o carregamento (pode levar alguns segundos)
4. Veja o Top 10 em destaque
5. Clique em **Ouvir no Spotify** para abrir a música
6. Expanda "Ver Top 100 Completo" para ver todas as músicas

## 📊 Histórico de Commits

```bash
git log --oneline
```

Commits semânticos seguindo Conventional Commits:
- `feat`: Nova funcionalidade
- `build`: Mudanças em dependências
- `chore`: Tarefas de manutenção
- `docs`: Documentação

## 🔗 Publicar no GitHub

```bash
# Criar repositório no GitHub primeiro, depois:
git remote add origin https://github.com/lazarorx/billboard-spotify-app.git
git branch -M main
git push -u origin main
```
