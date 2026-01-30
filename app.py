import streamlit as st
import billboard
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Billboard Top Songs",
    page_icon="🎵",
    layout="wide"
)

# Inicializar Spotify
@st.cache_resource
def init_spotify():
    """Inicializa o cliente do Spotify"""
    try:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            st.error("⚠️ Credenciais do Spotify não configuradas!")
            st.info("Configure o arquivo .env com suas credenciais do Spotify Developer")
            return None
            
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        st.error(f"Erro ao conectar com Spotify: {str(e)}")
        return None

def search_spotify_track(sp, song_name, artist_name):
    """Busca uma música no Spotify e retorna o link"""
    if not sp:
        return None
    
    try:
        query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return track['external_urls']['spotify']
        return None
    except Exception as e:
        return None

def get_billboard_chart(date_str):
    """Obtém o chart da Billboard para uma data específica"""
    try:
        chart = billboard.ChartData('hot-100', date=date_str)
        return chart
    except Exception as e:
        st.error(f"Erro ao buscar dados da Billboard: {str(e)}")
        return None

# Interface principal
st.title("🎵 Billboard Top Songs nos EUA")
st.markdown("### Descubra as músicas mais ouvidas e ouça no Spotify!")

# Sidebar para seleção de data
st.sidebar.header("📅 Selecione a Data")
st.sidebar.markdown("Escolha o mês e ano para ver o Top da Billboard")

# Seleção de ano e mês
current_year = datetime.now().year
year = st.sidebar.selectbox(
    "Ano",
    range(current_year, 1957, -1),
    index=0
)

month = st.sidebar.selectbox(
    "Mês",
    range(1, 13),
    format_func=lambda x: datetime(2000, x, 1).strftime('%B')
)

# Botão para buscar
if st.sidebar.button("🔍 Buscar Top Songs", type="primary"):
    # Formatar data
    date_str = f"{year}-{month:02d}-01"
    
    # Inicializar Spotify
    sp = init_spotify()
    
    # Buscar chart da Billboard
    with st.spinner("Buscando dados da Billboard..."):
        chart = get_billboard_chart(date_str)
    
    if chart:
        st.success(f"✅ Top 100 da Billboard - {chart.date}")
        
        # Criar lista de músicas
        songs_data = []
        
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, entry in enumerate(chart):
            status_text.text(f"Processando música {idx + 1} de {len(chart)}...")
            
            # Buscar link do Spotify
            spotify_link = search_spotify_track(sp, entry.title, entry.artist) if sp else None
            
            songs_data.append({
                'Posição': entry.rank,
                'Música': entry.title,
                'Artista': entry.artist,
                'Semanas no Chart': entry.weeks if entry.weeks else 'N/A',
                'Link Spotify': spotify_link if spotify_link else 'Não encontrado'
            })
            
            progress_bar.progress((idx + 1) / len(chart))
        
        status_text.empty()
        progress_bar.empty()
        
        # Exibir resultados
        st.markdown("---")
        st.subheader(f"🏆 Top {len(songs_data)} Músicas")
        
        # Mostrar top 10 em destaque
        st.markdown("### 🌟 Top 10")
        for song in songs_data[:10]:
            col1, col2, col3 = st.columns([1, 4, 2])
            
            with col1:
                st.markdown(f"### #{song['Posição']}")
            
            with col2:
                st.markdown(f"**{song['Música']}**")
                st.markdown(f"*{song['Artista']}*")
                st.caption(f"Semanas no chart: {song['Semanas no Chart']}")
            
            with col3:
                if song['Link Spotify'] != 'Não encontrado':
                    st.link_button("🎧 Ouvir no Spotify", song['Link Spotify'])
                else:
                    st.caption("Link não disponível")
            
            st.markdown("---")
        
        # Tabela completa expansível
        with st.expander("📊 Ver Top 100 Completo"):
            df = pd.DataFrame(songs_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

else:
    # Tela inicial
    st.info("👈 Use o menu lateral para selecionar uma data e buscar o Top da Billboard!")
    
    st.markdown("""
    ### Como usar:
    1. Selecione o **ano** e **mês** no menu lateral
    2. Clique em **Buscar Top Songs**
    3. Aguarde enquanto buscamos as músicas e os links do Spotify
    4. Explore o Top 10 em destaque ou veja a lista completa
    5. Clique em **Ouvir no Spotify** para abrir a música
    
    ### 📝 Nota:
    Para usar os links do Spotify, você precisa configurar as credenciais da API do Spotify no arquivo `.env`
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Desenvolvido com ❤️ usando Streamlit | Dados: Billboard & Spotify</p>
    </div>
    """,
    unsafe_allow_html=True
)
