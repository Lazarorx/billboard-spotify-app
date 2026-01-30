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
        
        # Calcular estatísticas
        df = pd.DataFrame(songs_data)
        total_songs = len(songs_data)
        
        # Artista mais frequente
        artist_counts = df['Artista'].value_counts()
        top_artist = artist_counts.index[0] if len(artist_counts) > 0 else "N/A"
        top_artist_count = artist_counts.iloc[0] if len(artist_counts) > 0 else 0
        
        # Média de semanas no chart
        weeks_list = [int(s['Semanas no Chart']) for s in songs_data if s['Semanas no Chart'] != 'N/A']
        avg_weeks = sum(weeks_list) / len(weeks_list) if weeks_list else 0
        
        # Links do Spotify disponíveis
        spotify_available = sum(1 for s in songs_data if s['Link Spotify'] != 'Não encontrado')
        
        # Exibir métricas
        st.markdown("---")
        st.markdown("### 📊 Estatísticas do Chart")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                <h2 style='color: white; margin: 0;'>{total_songs}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>Músicas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                <h2 style='color: white; margin: 0;'>{top_artist_count}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.85em;'>{top_artist}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                <h2 style='color: white; margin: 0;'>{avg_weeks:.1f}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>Média de Semanas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                <h2 style='color: white; margin: 0;'>{spotify_available}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>Links Spotify</p>
            </div>
            """, unsafe_allow_html=True)
        
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
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 20px; text-align: center;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin: 20px 0;'>
        <h2 style='color: white; margin: 0;'>👋 Bem-vindo!</h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.1em; margin: 10px 0 0 0;'>
            Use o menu lateral para começar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cards de instruções
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 15px; height: 100%;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0 0 15px 0;'>🎵 Como usar</h3>
            <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px;'>
                <ol style='color: #1F2937; margin: 0; padding-left: 20px;'>
                    <li style='margin: 10px 0;'>Selecione o <strong>ano</strong> e <strong>mês</strong> no menu lateral</li>
                    <li style='margin: 10px 0;'>Clique em <strong>Buscar Top Songs</strong></li>
                    <li style='margin: 10px 0;'>Aguarde o carregamento dos dados</li>
                    <li style='margin: 10px 0;'>Explore o Top 10 em destaque</li>
                    <li style='margin: 10px 0;'>Clique em <strong>Ouvir no Spotify</strong></li>
                </ol>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px; border-radius: 15px; height: 100%;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0 0 15px 0;'>⚙️ Configuração</h3>
            <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px;'>
                <p style='color: #1F2937; margin: 0 0 10px 0;'>
                    <strong>📝 Nota Importante:</strong>
                </p>
                <p style='color: #6B7280; margin: 0; line-height: 1.6;'>
                    Para usar os links do Spotify, você precisa configurar as credenciais 
                    da API do Spotify no arquivo <code>.env</code>
                </p>
                <p style='color: #6B7280; margin: 15px 0 0 0; line-height: 1.6;'>
                    Veja o arquivo <code>SETUP.md</code> para instruções detalhadas.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recursos disponíveis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                padding: 25px; border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <h3 style='color: white; margin: 0 0 15px 0;'>✨ Recursos</h3>
        <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px;'>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 2em; margin-bottom: 10px;'>📊</div>
                    <strong style='color: #1F2937;'>Estatísticas</strong>
                    <p style='color: #6B7280; font-size: 0.9em; margin: 5px 0 0 0;'>
                        Métricas detalhadas do chart
                    </p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 2em; margin-bottom: 10px;'>🎧</div>
                    <strong style='color: #1F2937;'>Links Spotify</strong>
                    <p style='color: #6B7280; font-size: 0.9em; margin: 5px 0 0 0;'>
                        Ouça as músicas diretamente
                    </p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 2em; margin-bottom: 10px;'>💾</div>
                    <strong style='color: #1F2937;'>Exportação</strong>
                    <p style='color: #6B7280; font-size: 0.9em; margin: 5px 0 0 0;'>
                        Baixe em CSV ou JSON
                    </p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 2em; margin-bottom: 10px;'>🏆</div>
                    <strong style='color: #1F2937;'>Top 100</strong>
                    <p style='color: #6B7280; font-size: 0.9em; margin: 5px 0 0 0;'>
                        Lista completa da Billboard
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
