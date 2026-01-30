import streamlit as st
import billboard
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import json

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Billboard Top Songs",
    page_icon="🎵",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    /* Estilo do título principal */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Animação hover nos cards */
    div[style*='background: linear-gradient'] {
        transition: transform 0.3s ease;
    }
    
    div[style*='background: linear-gradient']:hover {
        transform: translateY(-5px);
    }
    
    /* Estilo dos botões */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* Estilo da sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

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

def get_position_badge(position):
    """Retorna um badge HTML colorido baseado na posição"""
    if position == 1:
        return """
        <div style='display: inline-block; background: linear-gradient(135deg, #FFD700, #FFA500); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(255, 215, 0, 0.3);'>
            🥇 #1
        </div>
        """
    elif position == 2:
        return """
        <div style='display: inline-block; background: linear-gradient(135deg, #C0C0C0, #A8A8A8); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(192, 192, 192, 0.3);'>
            🥈 #2
        </div>
        """
    elif position == 3:
        return """
        <div style='display: inline-block; background: linear-gradient(135deg, #CD7F32, #B8860B); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(205, 127, 50, 0.3);'>
            🥉 #3
        </div>
        """
    elif position <= 10:
        return f"""
        <div style='display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);'>
            ⭐ #{position}
        </div>
        """
    else:
        return f"""
        <div style='display: inline-block; background: linear-gradient(135deg, #6B7280, #4B5563); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(107, 114, 128, 0.3);'>
            #{position}
        </div>
        """

def create_song_card(song, show_spotify_button=True):
    """Cria um card visual para uma música"""
    position = song['Posição']
    
    # Definir gradiente baseado na posição
    if position == 1:
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    elif position <= 3:
        gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    elif position <= 10:
        gradient = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    else:
        gradient = "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
    
    spotify_button = ""
    if show_spotify_button and song['Link Spotify'] != 'Não encontrado':
        spotify_button = f"""
        <a href="{song['Link Spotify']}" target="_blank" style="text-decoration: none;">
            <div style='background: #1DB954; color: white; padding: 10px 20px; 
                        border-radius: 25px; text-align: center; font-weight: bold;
                        margin-top: 15px; cursor: pointer; transition: all 0.3s;
                        box-shadow: 0 4px 6px rgba(29, 185, 84, 0.3);'>
                🎧 Ouvir no Spotify
            </div>
        </a>
        """
    elif show_spotify_button:
        spotify_button = """
        <div style='background: #6B7280; color: white; padding: 10px 20px; 
                    border-radius: 25px; text-align: center; font-weight: bold;
                    margin-top: 15px; opacity: 0.6;'>
            Link não disponível
        </div>
        """
    
    card_html = f"""
    <div style='background: {gradient}; padding: 25px; border-radius: 15px; 
                margin: 15px 0; box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                transition: transform 0.3s;'>
        <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px;'>
            {get_position_badge(position)}
            <h3 style='margin: 15px 0 5px 0; color: #1F2937;'>{song['Música']}</h3>
            <p style='color: #6B7280; font-size: 1.1em; margin: 5px 0;'>
                <strong>🎤 {song['Artista']}</strong>
            </p>
            <p style='color: #9CA3AF; font-size: 0.9em; margin: 10px 0 0 0;'>
                📊 {song['Semanas no Chart']} semanas no chart
            </p>
            {spotify_button}
        </div>
    </div>
    """
    
    return card_html

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
        
        # Mostrar top 10 em destaque com cards
        st.markdown("### 🌟 Top 10")
        
        for song in songs_data[:10]:
            st.markdown(create_song_card(song), unsafe_allow_html=True)
        
        # Tabela completa expansível
        with st.expander("📊 Ver Top 100 Completo"):
            df = pd.DataFrame(songs_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Opções de exportação
        st.markdown("---")
        st.subheader("💾 Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Exportar CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=f"billboard_top100_{year}_{month:02d}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Exportar JSON
            json_data = json.dumps(songs_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Baixar JSON",
                data=json_data,
                file_name=f"billboard_top100_{year}_{month:02d}.json",
                mime="application/json",
                use_container_width=True
            )

else:
    # Tela inicial
    st.info(" Use o menu lateral para selecionar uma data e buscar o Top da Billboard!")
    
    st.markdown("""
    ### Como usar:
    1. Selecione o **ano** e **mês** no menu lateral
    2. Clique em **Buscar Top Songs**
    3. Aguarde enquanto buscamos as músicas e os links do Spotify
    4. Explore o Top 10 em destaque ou veja a lista completa
    5. Clique em **Ouvir no Spotify** para abrir a música
    
    ###  Nota:
    Para usar os links do Spotify, você precisa configurar as credenciais da API do Spotify no arquivo `.env`
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Desenvolvido por Lázaro Xavier usando Streamlit | Dados: Billboard & Spotify</p>
    </div>
    """,
    unsafe_allow_html=True
)
