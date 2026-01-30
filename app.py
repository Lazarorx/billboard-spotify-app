import streamlit as st
import billboard
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
import plotly.graph_objects as go

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Billboard Top Songs",
    page_icon="�",
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
        transition: transform 0.3s ease;
        cursor: default;
    }
    
    h1:hover {
        transform: scale(1.02);
    }
    
    /* Forçar texto branco no cabeçalho com gradiente */
    div[style*='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)'] h1 {
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: white !important;
        color: white !important;
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
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 0 0 15px 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Estilo dos selectbox na sidebar */
    [data-testid="stSidebar"] .stSelectbox label {
        color: #1F2937 !important;
        font-weight: 600;
        font-size: 1.05em;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div {
        background: white;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div:hover {
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        transform: translateY(-1px);
    }
    
    /* Estilo do botão na sidebar */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: bold;
        font-size: 1.05em;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Animação suave na sidebar */
    [data-testid="stSidebar"] * {
        transition: all 0.3s ease;
    }
    
    /* Estilo das imagens dos artistas */
    [data-testid="stImage"] img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
        width: 100%;
        height: 250px;
        object-fit: cover;
        object-position: center;
    }
    
    [data-testid="stImage"]:hover img {
        transform: scale(1.05);
    }
    /* Efeito hover na logo do cabeçalho */
    .logo-header {
        width: 150px;
        height: auto;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    .logo-header:hover {
        transform: scale(1.3) rotate(360deg);
        filter: drop-shadow(0 0 30px rgba(255,255,255,0.9)) 
                drop-shadow(0 0 50px rgba(102,126,234,0.7)) 
                brightness(1.3);
    }
    
    /* Efeito hover na logo da sidebar */
    .logo-sidebar {
        width: 280px;
        height: auto;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .logo-sidebar:hover {
        transform: scale(1.15) rotate(360deg);
        filter: drop-shadow(0 0 30px rgba(255,255,255,0.9)) 
                drop-shadow(0 0 50px rgba(102,126,234,0.7)) 
                brightness(1.3);
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
            return None
            
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        return None

def search_spotify_track(sp, song_name, artist_name):
    """Busca uma música no Spotify e retorna o link"""
    # Criar link de busca direto do Spotify (não depende de API)
    # Formato: https://open.spotify.com/search/artista%20musica
    import urllib.parse
    
    query = f"{artist_name} {song_name}"
    encoded_query = urllib.parse.quote(query)
    search_link = f"https://open.spotify.com/search/{encoded_query}"
    
    return search_link

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
        return f"""
        <div style='display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);'>
            #{position}
        </div>
        """
    elif position == 2:
        return f"""
        <div style='display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3); opacity: 0.9;'>
            #{position}
        </div>
        """
    elif position == 3:
        return f"""
        <div style='display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3); opacity: 0.8;'>
            #{position}
        </div>
        """
    elif position <= 10:
        return f"""
        <div style='display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); 
                    padding: 8px 16px; border-radius: 20px; font-weight: bold; 
                    color: white; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3); opacity: 0.7;'>
            #{position}
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
    
    # Limpar caracteres que podem quebrar HTML (sem escape completo)
    musica = str(song['Música']).replace('"', '&quot;').replace("'", '&#39;')
    artista = str(song['Artista']).replace('"', '&quot;').replace("'", '&#39;')
    semanas = str(song['Semanas no Chart'])
    
    # Gradiente padrão roxo/azul para todos
    gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    
    spotify_button = ""
    if show_spotify_button and song['Link Spotify'] != 'Não encontrado':
        spotify_link = str(song['Link Spotify'])
        spotify_button = f"""
        <a href="{spotify_link}" target="_blank" style="text-decoration: none;">
            <div style='background: #667eea; color: white; padding: 10px 20px; 
                        border-radius: 25px; text-align: center; font-weight: bold;
                        margin-top: 15px; cursor: pointer; transition: all 0.3s;
                        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);'>
                Buscar no Spotify
            </div>
        </a>
        """
    elif show_spotify_button:
        spotify_button = ""
    
    # Obter badge da posição
    badge_html = get_position_badge(position)
    
    card_html = f"""
    <div style='background: {gradient}; padding: 25px; border-radius: 15px; 
                margin: 15px 0; box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                transition: transform 0.3s;'>
        <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px;'>
            {badge_html}
            <h3 style='margin: 15px 0 5px 0; color: #1F2937;'>{musica}</h3>
            <p style='color: #6B7280; font-size: 1.1em; margin: 5px 0;'>
                <strong>{artista}</strong>
            </p>
            <p style='color: #9CA3AF; font-size: 0.9em; margin: 10px 0 0 0;'>
                {semanas} semanas no chart
            </p>
            {spotify_button}
        </div>
    </div>
    """
    
    return card_html

# Interface principal
# Carregar logo para o cabeçalho
try:
    from PIL import Image
    import base64
    from io import BytesIO
    
    logo_header = Image.open("assets/logo.jpg")
    buffered_header = BytesIO()
    logo_header.save(buffered_header, format="PNG", quality=100)
    img_str_header = base64.b64encode(buffered_header.getvalue()).decode()
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px 40px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <div style='display: flex; align-items: center; justify-content: center; gap: 30px;'>
            <img src="data:image/png;base64,{img_str_header}" class="logo-header">
            <div>
                <div style='margin: 0; font-size: 2.8em; font-weight: 900; 
                           letter-spacing: 2px;
                           cursor: default;
                           animation: glow 2s ease-in-out infinite, float 3s ease-in-out infinite;
                           background: linear-gradient(90deg, 
                                       rgba(255,255,255,0.8) 0%, 
                                       rgba(255,255,255,1) 25%, 
                                       rgba(255,255,255,0.8) 50%, 
                                       rgba(255,255,255,1) 75%, 
                                       rgba(255,255,255,0.8) 100%);
                           background-size: 200% auto;
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;
                           background-clip: text;
                           animation: shimmer 3s linear infinite, glow 2s ease-in-out infinite, float 3s ease-in-out infinite;
                           filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
                           transition: transform 0.3s ease, letter-spacing 0.3s ease;'
                     onmouseover="this.style.transform='scale(1.1)'; this.style.letterSpacing='8px'"
                     onmouseout="this.style.transform='scale(1)'; this.style.letterSpacing='2px'">
                    Billboard Explorer
                </div>
                <p style='color: rgba(255,255,255,0.95); font-size: 1.2em; margin: 8px 0 0 0;
                          text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>
                    Descubra as músicas mais populares e ouça no Spotify
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
except:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px 40px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <div style='display: flex; align-items: center; justify-content: center; gap: 20px;'>
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" fill="white" opacity="0.95"/>
            </svg>
            <div>
                <div style='margin: 0; font-size: 2.8em; font-weight: 900; 
                           letter-spacing: 2px;
                           cursor: default;
                           animation: glow 2s ease-in-out infinite, float 3s ease-in-out infinite;
                           background: linear-gradient(90deg, 
                                       rgba(255,255,255,0.8) 0%, 
                                       rgba(255,255,255,1) 25%, 
                                       rgba(255,255,255,0.8) 50%, 
                                       rgba(255,255,255,1) 75%, 
                                       rgba(255,255,255,0.8) 100%);
                           background-size: 200% auto;
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;
                           background-clip: text;
                           animation: shimmer 3s linear infinite, glow 2s ease-in-out infinite, float 3s ease-in-out infinite;
                           filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
                           transition: transform 0.3s ease, letter-spacing 0.3s ease;'
                     onmouseover="this.style.transform='scale(1.1)'; this.style.letterSpacing='8px'"
                     onmouseout="this.style.transform='scale(1)'; this.style.letterSpacing='2px'">
                    Billboard Explorer
                </div>
                <p style='color: rgba(255,255,255,0.95); font-size: 1.2em; margin: 8px 0 0 0;
                          text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>
                    Descubra as músicas mais populares e ouça no Spotify
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para seleção de data
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px 0 5px 0;'>
""", unsafe_allow_html=True)

# Logo
try:
    from PIL import Image
    logo = Image.open("assets/logo.jpg")
    # Usar HTML para melhor controle de qualidade
    import base64
    from io import BytesIO
    
    buffered = BytesIO()
    logo.save(buffered, format="PNG", quality=100)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    st.sidebar.markdown(f"""
    <div style='text-align: center; margin-bottom: 15px;'>
        <img src="data:image/png;base64,{img_str}" class="logo-sidebar">
    </div>
    """, unsafe_allow_html=True)
except:
    st.sidebar.markdown("""
    <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 20px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">
        <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" fill="white" opacity="0.95"/>
    </svg>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

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

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Botão para buscar
if st.sidebar.button("Buscar Top Songs", type="primary"):
    # Formatar data
    date_str = f"{year}-{month:02d}-01"
    
    # Inicializar Spotify
    sp = init_spotify()
    
    # Buscar chart da Billboard
    with st.spinner(f"🎵 Buscando ranking da Billboard para {datetime(year, month, 1).strftime('%B/%Y')}..."):
        chart = get_billboard_chart(date_str)
    
    if chart:
        # Criar lista de músicas
        songs_data = []
        
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Processar todas as músicas primeiro (sem Spotify)
        for idx, entry in enumerate(chart):
            status_text.text(f"📊 Carregando música {idx + 1} de {len(chart)}...")
            
            songs_data.append({
                'Posição': entry.rank,
                'Música': entry.title,
                'Artista': entry.artist,
                'Semanas no Chart': entry.weeks if entry.weeks else 'N/A',
                'Link Spotify': 'Não encontrado'
            })
            
            progress_bar.progress((idx + 1) / len(chart))
        
        status_text.empty()
        progress_bar.empty()
        
        # Adicionar links de busca do Spotify para todas as músicas
        for idx in range(len(songs_data)):
            song = songs_data[idx]
            spotify_link = search_spotify_track(None, song['Música'], song['Artista'])
            songs_data[idx]['Link Spotify'] = spotify_link
        
        # Header com informações do chart
        month_name = datetime(year, month, 1).strftime('%B')
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 20px; text-align: center;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin: 20px 0 30px 0;'>
            <h2 style='color: white; margin: 0; font-size: 2em;'>🎧 Top 10 – {month_name} {year}</h2>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1em; margin: 10px 0 0 0;'>
                Billboard Hot 100 Chart
            </p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # Links do Spotify disponíveis (agora sempre 100%)
        spotify_available = len(songs_data)
        
        # Exibir métricas
        st.markdown("### Estatísticas do Chart")
        
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
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1); opacity: 0.9;'>
                <h2 style='color: white; margin: 0;'>{top_artist_count}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.85em;'>{top_artist}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1); opacity: 0.8;'>
                <h2 style='color: white; margin: 0;'>{avg_weeks:.1f}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>Média de Semanas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1); opacity: 0.7;'>
                <h2 style='color: white; margin: 0;'>{spotify_available}</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>Links Disponíveis</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de Top 10 Artistas
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Top 10 Artistas do Período")
        
        # Contar artistas
        artist_counts = df['Artista'].value_counts().head(10)
        
        # Criar gráfico de barras com Plotly
        fig = go.Figure(data=[
            go.Bar(
                x=artist_counts.values,
                y=artist_counts.index,
                orientation='h',
                marker=dict(
                    color=artist_counts.values,
                    colorscale=[[0, '#764ba2'], [1, '#667eea']],
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=artist_counts.values,
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>%{x} músicas<extra></extra>'
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Arial', size=12, color='#1F2937'),
            xaxis=dict(
                title='Número de Músicas',
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                zeroline=False
            ),
            yaxis=dict(
                title='',
                showgrid=False,
                autorange='reversed'
            ),
            margin=dict(l=20, r=20, t=20, b=40),
            height=400,
            hoverlabel=dict(
                bgcolor='white',
                font_size=13,
                font_family='Arial'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Expander com gráficos extras
        with st.expander("📊 Ver Mais Estatísticas"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("#### Distribuição por Semanas no Chart")
                # Gráfico de pizza
                weeks_ranges = pd.cut(
                    [int(s['Semanas no Chart']) for s in songs_data if s['Semanas no Chart'] != 'N/A'],
                    bins=[0, 5, 10, 20, 50, 100],
                    labels=['1-5 semanas', '6-10 semanas', '11-20 semanas', '21-50 semanas', '50+ semanas']
                )
                weeks_dist = weeks_ranges.value_counts()
                
                fig_pie = go.Figure(data=[
                    go.Pie(
                        labels=weeks_dist.index,
                        values=weeks_dist.values,
                        hole=0.4,
                        marker=dict(
                            colors=['#667eea', '#764ba2', '#8e54e9', '#9d64e8', '#ac74e7']
                        ),
                        textinfo='label+percent',
                        hovertemplate='<b>%{label}</b><br>%{value} músicas<extra></extra>'
                    )
                ])
                
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Arial', size=11),
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=300,
                    showlegend=True
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_b:
                st.markdown("#### Top 5 Artistas - Detalhes")
                top5_artists = artist_counts.head(5)
                
                for idx, (artist, count) in enumerate(top5_artists.items(), 1):
                    percentage = (count / total_songs) * 100
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 15px; border-radius: 10px; margin-bottom: 10px;
                                opacity: {1 - (idx * 0.1)};'>
                        <div style='color: white;'>
                            <strong style='font-size: 1.1em;'>#{idx} {artist}</strong><br>
                            <span style='font-size: 0.9em;'>{count} músicas ({percentage:.1f}% do chart)</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Exibir resultados
        st.markdown("---")
        
        # Mostrar top 10 em destaque com cards
        
        for song in songs_data[:10]:
            card_html = create_song_card(song)
            st.html(card_html)
        
        # Tabela completa expansível
        with st.expander("Ver Top 100 Completo"):
            df = pd.DataFrame(songs_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Opções de exportação
        st.markdown("---")
        st.subheader("Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Exportar CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv,
                file_name=f"billboard_top100_{year}_{month:02d}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Exportar JSON
            json_data = json.dumps(songs_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="Baixar JSON",
                data=json_data,
                file_name=f"billboard_top100_{year}_{month:02d}.json",
                mime="application/json",
                use_container_width=True
            )

else:
    # Tela inicial - Hero Section com efeitos
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 60px 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 12px 24px rgba(0,0,0,0.3); margin: 30px 0 40px 0;
                position: relative; overflow: hidden;
                animation: fadeIn 0.8s ease-in;'>
        <div style='position: absolute; top: -50px; right: -50px; width: 200px; height: 200px;
                    background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(40px);'></div>
        <div style='position: absolute; bottom: -30px; left: -30px; width: 150px; height: 150px;
                    background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px);'></div>
        <div style='position: relative; z-index: 2;'>
            <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 20px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">
                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" fill="white" opacity="0.9"/>
            </svg>
            <h1 style='color: white; 
                       margin: 0; 
                       font-size: 3.5em; 
                       font-weight: 900; 
                       letter-spacing: 2px;
                       cursor: default;
                       animation: glow 2s ease-in-out infinite, float 3s ease-in-out infinite;
                       background: linear-gradient(90deg, 
                                   rgba(255,255,255,0.8) 0%, 
                                   rgba(255,255,255,1) 25%, 
                                   rgba(255,255,255,0.8) 50%, 
                                   rgba(255,255,255,1) 75%, 
                                   rgba(255,255,255,0.8) 100%);
                       background-size: 200% auto;
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       background-clip: text;
                       animation: shimmer 3s linear infinite, glow 2s ease-in-out infinite, float 3s ease-in-out infinite;
                       filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
                       transition: transform 0.3s ease, letter-spacing 0.3s ease;'
                 onmouseover="this.style.transform='scale(1.1)'; this.style.letterSpacing='8px'"
                 onmouseout="this.style.transform='scale(1)'; this.style.letterSpacing='2px'">
                Billboard Top Songs
            </h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3em; margin: 25px 0 35px 0; line-height: 1.6;
                      text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                Explore o ranking Billboard nos EUA desde 1958<br>
                Descubra os maiores hits de cada época
            </p>
            <div style='display: inline-block; background: rgba(255,255,255,0.25); 
                        padding: 18px 35px; border-radius: 50px; backdrop-filter: blur(10px);
                        border: 2px solid rgba(255,255,255,0.3); transition: all 0.3s;'
                 onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.transform='scale(1.05)'"
                 onmouseout="this.style.background='rgba(255,255,255,0.25)'; this.style.transform='scale(1)'">
                <p style='color: white; margin: 0; font-size: 1.15em; font-weight: 600;
                          text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                    ◀ Comece selecionando uma data
                </p>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        @keyframes shimmer {
            0% {
                background-position: -1000px 0;
            }
            100% {
                background-position: 1000px 0;
            }
        }
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 10px rgba(255,255,255,0.8),
                             0 0 20px rgba(255,255,255,0.6),
                             0 0 30px rgba(255,255,255,0.4),
                             0 0 40px rgba(102,126,234,0.6),
                             0 0 70px rgba(118,75,162,0.5),
                             0 0 80px rgba(102,126,234,0.4);
            }
            50% {
                text-shadow: 0 0 20px rgba(255,255,255,1),
                             0 0 30px rgba(255,255,255,0.8),
                             0 0 40px rgba(255,255,255,0.6),
                             0 0 50px rgba(102,126,234,0.8),
                             0 0 80px rgba(118,75,162,0.7),
                             0 0 100px rgba(102,126,234,0.6);
            }
        }
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Cards de estatísticas visuais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 40px 30px; border-radius: 15px; 
                    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border-top: 5px solid #667eea; height: 100%;'>
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 15px;">
                <defs>
                    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <path d="M3 13h2v8H3v-8zm4-6h2v14H7V7zm4-4h2v18h-2V3zm4 9h2v9h-2v-9zm4-3h2v12h-2V9z" fill="url(#grad1)"/>
            </svg>
            <h3 style='color: #1F2937; margin: 0 0 10px 0;'>Top 100</h3>
            <p style='color: #6B7280; margin: 0; line-height: 1.6;'>
                Rankings semanais das músicas mais populares nos EUA
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 40px 30px; border-radius: 15px; 
                    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border-top: 5px solid #764ba2; height: 100%;'>
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 15px;">
                <defs>
                    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" fill="url(#grad2)"/>
            </svg>
            <h3 style='color: #1F2937; margin: 0 0 10px 0;'>Desde 1958</h3>
            <p style='color: #6B7280; margin: 0; line-height: 1.6;'>
                Mais de 60 anos de história musical documentada
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 40px 30px; border-radius: 15px; 
                    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border-top: 5px solid #667eea; height: 100%;'>
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 15px;">
                <defs>
                    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <path d="M12 1c-4.97 0-9 4.03-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7c0-4.97-4.03-9-9-9z" fill="url(#grad3)"/>
            </svg>
            <h3 style='color: #1F2937; margin: 0 0 10px 0;'>Spotify</h3>
            <p style='color: #6B7280; margin: 0; line-height: 1.6;'>
                Links diretos para ouvir suas músicas favoritas
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de destaques com fotos
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 50px 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-bottom: 30px;'>
        <h2 style='color: white; margin: 0; font-size: 2.2em; font-weight: bold;
                   text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
            Artistas Lendários que Dominaram as Paradas
        </h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.1em; margin: 15px 0 0 0;'>
            Conheça os maiores nomes da história da música
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de artistas com st.columns
    artists = [
        {"name": "The Beatles", "image": "assets/beatles.jpg", "hits": "20 músicas #1", "color": "#667eea"},
        {"name": "Michael Jackson", "image": "assets/michael-jackson.jpg", "hits": "13 músicas #1", "color": "#f093fb"},
        {"name": "Madonna", "image": "assets/madonna.jpg", "hits": "12 músicas #1", "color": "#4facfe"},
        {"name": "Elvis Presley", "image": "assets/elvis.jpg", "hits": "18 músicas #1", "color": "#fa709a"},
        {"name": "Taylor Swift", "image": "assets/taylor-swift.jpg", "hits": "9 músicas #1", "color": "#30cfd0"},
        {"name": "Drake", "image": "assets/drake.jpg", "hits": "11 músicas #1", "color": "#a8edea"}
    ]
    
    # Primeira linha
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 4px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <div style='background: white; padding: 15px; border-radius: 12px;'>
        """, unsafe_allow_html=True)
        st.image(artists[0]["image"], use_container_width=True)
        st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                   -webkit-background-clip: text;
                                   -webkit-text-fill-color: transparent;
                                   background-clip: text;
                                   font-size: 1.3em;'>{artists[0]["name"]}</strong><br>
                    <span style='color: #6B7280; font-size: 0.95em; font-weight: 500;'>{artists[0]["hits"]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 4px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <div style='background: white; padding: 15px; border-radius: 12px;'>
        """, unsafe_allow_html=True)
        st.image(artists[1]["image"], use_container_width=True)
        st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                   -webkit-background-clip: text;
                                   -webkit-text-fill-color: transparent;
                                   background-clip: text;
                                   font-size: 1.3em;'>{artists[1]["name"]}</strong><br>
                    <span style='color: #6B7280; font-size: 0.95em; font-weight: 500;'>{artists[1]["hits"]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 4px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <div style='background: white; padding: 15px; border-radius: 12px;'>
        """, unsafe_allow_html=True)
        st.image(artists[2]["image"], use_container_width=True)
        st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                   -webkit-background-clip: text;
                                   -webkit-text-fill-color: transparent;
                                   background-clip: text;
                                   font-size: 1.3em;'>{artists[2]["name"]}</strong><br>
                    <span style='color: #6B7280; font-size: 0.95em; font-weight: 500;'>{artists[2]["hits"]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Segunda linha
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 4px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <div style='background: white; padding: 15px; border-radius: 12px;'>
        """, unsafe_allow_html=True)
        st.image(artists[3]["image"], use_container_width=True)
        st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                   -webkit-background-clip: text;
                                   -webkit-text-fill-color: transparent;
                                   background-clip: text;
                                   font-size: 1.3em;'>{artists[3]["name"]}</strong><br>
                    <span style='color: #6B7280; font-size: 0.95em; font-weight: 500;'>{artists[3]["hits"]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 4px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <div style='background: white; padding: 15px; border-radius: 12px;'>
        """, unsafe_allow_html=True)
        st.image(artists[4]["image"], use_container_width=True)
        st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                   -webkit-background-clip: text;
                                   -webkit-text-fill-color: transparent;
                                   background-clip: text;
                                   font-size: 1.3em;'>{artists[4]["name"]}</strong><br>
                    <span style='color: #6B7280; font-size: 0.95em; font-weight: 500;'>{artists[4]["hits"]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 4px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <div style='background: white; padding: 15px; border-radius: 12px;'>
        """, unsafe_allow_html=True)
        st.image(artists[5]["image"], use_container_width=True)
        st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                   -webkit-background-clip: text;
                                   -webkit-text-fill-color: transparent;
                                   background-clip: text;
                                   font-size: 1.3em;'>{artists[5]["name"]}</strong><br>
                    <span style='color: #6B7280; font-size: 0.95em; font-weight: 500;'>{artists[5]["hits"]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 40px; border-radius: 15px; margin-top: 50px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; text-align: center;'>
        <div>
            <h3 style='color: white; margin: 0 0 10px 0; font-size: 1.1em;'>Desenvolvedor</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95em;'>
                Lázaro Xavier
            </p>
            <a href='https://github.com/Lazarorx' target='_blank' style='color: white; text-decoration: none; font-size: 0.9em; opacity: 0.8;'>
                @lazarorx
            </a>
        </div>
        <div>
            <h3 style='color: white; margin: 0 0 10px 0; font-size: 1.1em;'>Tecnologias</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95em;'>
                Python • Streamlit<br>
                Billboard API • Spotify API
            </p>
        </div>
        <div>
            <h3 style='color: white; margin: 0 0 10px 0; font-size: 1.1em;'>Fontes de Dados</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95em;'>
                Billboard Hot 100<br>
                Spotify Web API
            </p>
        </div>
    </div>
    <div style='text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);'>
        <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9em;'>
            © 2026 Billboard Explorer • Todos os direitos reservados
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
