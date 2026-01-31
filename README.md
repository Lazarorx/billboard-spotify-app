# Billboard Explorer

Aplicação web interativa para explorar o histórico da Billboard Hot 100, permitindo consultar as músicas mais populares dos EUA desde 1958, com integração ao Spotify para ouvir as faixas.

## Sobre o Projeto

Billboard Explorer é uma ferramenta que combina dados históricos da Billboard com links diretos para o Spotify, oferecendo uma experiência visual moderna para descobrir e explorar os maiores hits musicais de cada época.

A aplicação utiliza uma abordagem inovadora para integração com o Spotify: ao invés de depender da API (que requer autenticação e tem limites), gera links de busca diretos que funcionam 100% do tempo, sem necessidade de credenciais ou configuração adicional.

## Funcionalidades

- Consulta do Billboard Hot 100 por mês e ano (desde 1958)
- Visualização do Top 10 com cards visuais estilizados
- Links de busca diretos para o Spotify (100% de disponibilidade)
- Gráficos interativos com Plotly para análise de dados
- Estatísticas do chart (total de músicas, artista mais frequente, média de semanas)
- Exportação de dados em CSV e JSON
- Interface responsiva com design moderno
- Animações e efeitos visuais interativos

## Screenshots

### Tela Inicial
![Tela Inicial](screenshots/home.png)

### Visualização do Top 10
![Top 10](screenshots/top10.png)

### Cards de Músicas
![Cards](screenshots/cards.png)

## Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Streamlit**: Framework para interface web
- **billboard.py**: Biblioteca para acessar dados da Billboard
- **Plotly**: Biblioteca para gráficos interativos
- **Pandas**: Manipulação e análise de dados
- **Pillow**: Processamento de imagens

## Pré-requisitos

- Python 3.8 ou superior
- Conexão com internet

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Lazarorx/billboard-spotify-app.git
cd billboard-spotify-app
```

### 2. Crie um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

### Integração com Spotify

A aplicação utiliza **links de busca diretos** do Spotify, que não requerem autenticação ou configuração de API. Quando você clica em "Buscar no Spotify", o link abre automaticamente uma busca no Spotify com o nome da música e artista, funcionando 100% do tempo sem dependências externas.

**Vantagens desta abordagem:**
- ✅ Sem necessidade de credenciais ou configuração
- ✅ 100% de disponibilidade (não depende de APIs)
- ✅ Sem limites de requisições
- ✅ Funciona para qualquer período (1958-2026)

### Navegação

1. Use a sidebar para selecionar o mês e ano desejado
2. Clique em "Buscar Top Songs"
3. Visualize o Top 10 com cards estilizados
4. Clique em "Ouvir no Spotify" para abrir a música
5. Expanda "Ver Top 100 Completo" para a tabela completa
6. Exporte os dados em CSV ou JSON se desejar

## Estrutura do Projeto

```
billboard-spotify-app/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── .env.example          # Template de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Documentação
├── SETUP.md              # Guia de configuração detalhado
├── assets/               # Recursos visuais
│   ├── logo.jpg         # Logo da aplicação
│   ├── beatles.jpg      # Foto dos Beatles
│   ├── drake.jpg        # Foto do Drake
│   ├── elvis.jpg        # Foto do Elvis
│   ├── madonna.jpg      # Foto da Madonna
│   ├── michael-jackson.jpg  # Foto do Michael Jackson
│   └── taylor-swift.jpg     # Foto da Taylor Swift
└── screenshots/          # Capturas de tela (para README)
```

## Funcionalidades Detalhadas

### Busca de Rankings
- Seleção de qualquer mês/ano desde 1958
- Carregamento otimizado com feedback visual
- Cache de dados para melhor performance

### Integração Spotify
- Busca automática de links para o Top 10
- Links diretos que abrem no Spotify Web ou App
- Fallback gracioso quando links não estão disponíveis

### Visualização
- Cards com gradientes e badges de posição
- Informações de artista e tempo no chart
- Design responsivo e moderno
- Efeitos hover interativos

### Exportação
- Formato CSV para análise em Excel/Sheets
- Formato JSON para integração com outras aplicações
- Dados completos do Top 100

## Desenvolvimento

### Commits Semânticos

O projeto utiliza commits semânticos seguindo o padrão:

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação e estilo
- `refactor`: Refatoração de código
- `perf`: Melhorias de performance
- `test`: Testes
- `build`: Build e dependências
- `chore`: Tarefas gerais

### Histórico de Desenvolvimento

Veja o histórico completo de commits com:
```bash
git log --oneline --graph
```

## Solução de Problemas

### Links do Spotify não abrem
- Verifique sua conexão com internet
- Certifique-se de que o Spotify está instalado ou use o Spotify Web
- Tente abrir o link manualmente copiando a URL

### Erro ao carregar dados
- Verifique sua conexão com internet
- Tente uma data diferente (algumas datas antigas podem não ter dados)
- Reinicie a aplicação

### Imagens não aparecem
- Confirme que a pasta `assets/` contém todas as imagens
- Verifique as permissões de leitura dos arquivos
- Limpe o cache do Streamlit: `streamlit cache clear`

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## Roadmap

- [ ] Adicionar gráficos de evolução de artistas
- [ ] Implementar busca por artista específico
- [ ] Criar comparação entre diferentes períodos
- [ ] Adicionar player de preview do Spotify
- [ ] Implementar modo escuro
- [ ] Adicionar mais charts da Billboard (Rock, Country, etc)

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

**Lázaro Xavier**
- GitHub: [@Lazarorx](https://github.com/Lazarorx)
- Projeto: [Billboard Explorer](https://github.com/Lazarorx/billboard-spotify-app)

## Agradecimentos

- Billboard por disponibilizar os dados históricos
- Spotify pela API de música
- Comunidade Streamlit pelo framework incrível

---

Desenvolvido com dedicação por Lázaro Xavier | 2026
