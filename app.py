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
                Ouvir no Spotify
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
st.title("Billboard Top Songs nos EUA")
st.markdown("<p style='color: #6B7280; font-size: 1.2em; margin-top: -10px;'>Descubra as músicas mais ouvidas e ouça no Spotify</p>", unsafe_allow_html=True)

# Sidebar para seleção de data
st.sidebar.markdown("""
<div style='text-align: center; padding: 15px 0;'>
    <div style='font-size: 3em; margin-bottom: 10px;'>🎵</div>
    <h2 style='margin: 0; color: white; font-size: 1.5em;'>Selecione a Data</h2>
    <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 0.95em;'>
        Escolha o mês e ano
    </p>
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
        
        # Buscar links do Spotify apenas para o Top 10 (se configurado)
        if sp:
            progress_bar_spotify = st.progress(0)
            status_spotify = st.empty()
            status_spotify.text("🔗 Cruzando links com Spotify...")
            
            for idx in range(min(10, len(songs_data))):
                song = songs_data[idx]
                spotify_link = search_spotify_track(sp, song['Música'], song['Artista'])
                if spotify_link:
                    songs_data[idx]['Link Spotify'] = spotify_link
                progress_bar_spotify.progress((idx + 1) / 10)
            
            progress_bar_spotify.empty()
            status_spotify.empty()
        
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
        
        # Links do Spotify disponíveis
        spotify_available = sum(1 for s in songs_data if s['Link Spotify'] != 'Não encontrado')
        
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
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>Links Spotify</p>
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
            <div style='font-size: 4em; margin-bottom: 20px; animation: bounce 2s infinite;'>🎵</div>
            <h1 style='color: white; margin: 0; font-size: 3.5em; font-weight: bold; 
                       text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                       letter-spacing: 3px;'>
                BILLBOARD TOP SONGS
            </h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3em; margin: 25px 0 35px 0; line-height: 1.6;
                      text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                Explore as músicas mais ouvidas nos EUA desde 1958<br>
                Descubra os maiores hits de cada época
            </p>
            <div style='display: inline-block; background: rgba(255,255,255,0.25); 
                        padding: 18px 35px; border-radius: 50px; backdrop-filter: blur(10px);
                        border: 2px solid rgba(255,255,255,0.3); transition: all 0.3s;'
                 onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.transform='scale(1.05)'"
                 onmouseout="this.style.background='rgba(255,255,255,0.25)'; this.style.transform='scale(1)'">
                <p style='color: white; margin: 0; font-size: 1.15em; font-weight: 600;
                          text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                    ▶ Selecione uma data no menu lateral para começar
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
    </style>
    """, unsafe_allow_html=True)
    
    # Cards de estatísticas visuais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 40px 30px; border-radius: 15px; 
                    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border-top: 5px solid #667eea; height: 100%;'>
            <div style='font-size: 4em; margin-bottom: 15px;'>📊</div>
            <h3 style='color: #1F2937; margin: 0 0 10px 0;'>Top 100</h3>
            <p style='color: #6B7280; margin: 0; line-height: 1.6;'>
                Rankings semanais das músicas mais tocadas nos EUA
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 40px 30px; border-radius: 15px; 
                    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border-top: 5px solid #764ba2; height: 100%;'>
            <div style='font-size: 4em; margin-bottom: 15px;'>🎵</div>
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
            <div style='font-size: 4em; margin-bottom: 15px;'>🎧</div>
            <h3 style='color: #1F2937; margin: 0 0 10px 0;'>Spotify</h3>
            <p style='color: #6B7280; margin: 0; line-height: 1.6;'>
                Links diretos para ouvir suas músicas favoritas
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de destaques com fotos
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 50px 40px; border-radius: 20px; text-align: center;'>
        <h2 style='color: #1F2937; margin: 0 0 30px 0; font-size: 2em;'>
            Artistas Lendários que Dominaram as Paradas
        </h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
                    gap: 25px; margin-top: 30px;'>
            <div style='background: white; padding: 15px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s; cursor: pointer;'
                 onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 8px 20px rgba(102,126,234,0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
                <img src='assets/beatles.jpg' 
                     style='width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;'
                     onerror="this.src='https://via.placeholder.com/200x180/667eea/ffffff?text=Beatles'"/>
                <strong style='color: #667eea; font-size: 1.2em; display: block; margin-bottom: 5px;'>The Beatles</strong>
                <p style='color: #6B7280; font-size: 0.9em; margin: 0;'>20 músicas #1</p>
            </div>
            <div style='background: white; padding: 15px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s; cursor: pointer;'
                 onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 8px 20px rgba(240,147,251,0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
                <img src='assets/michael-jackson.jpg' 
                     style='width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;'
                     onerror="this.src='https://via.placeholder.com/200x180/f093fb/ffffff?text=MJ'"/>
                <strong style='color: #f093fb; font-size: 1.2em; display: block; margin-bottom: 5px;'>Michael Jackson</strong>
                <p style='color: #6B7280; font-size: 0.9em; margin: 0;'>13 músicas #1</p>
            </div>
            <div style='background: white; padding: 15px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s; cursor: pointer;'
                 onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 8px 20px rgba(79,172,254,0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
                <img src='assets/madonna.jpg' 
                     style='width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;'
                     onerror="this.src='https://via.placeholder.com/200x180/4facfe/ffffff?text=Madonna'"/>
                <strong style='color: #4facfe; font-size: 1.2em; display: block; margin-bottom: 5px;'>Madonna</strong>
                <p style='color: #6B7280; font-size: 0.9em; margin: 0;'>12 músicas #1</p>
            </div>
            <div style='background: white; padding: 15px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s; cursor: pointer;'
                 onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 8px 20px rgba(250,112,154,0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
                <img src='assets/elvis.jpg' 
                     style='width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;'
                     onerror="this.src='https://via.placeholder.com/200x180/fa709a/ffffff?text=Elvis'"/>
                <strong style='color: #fa709a; font-size: 1.2em; display: block; margin-bottom: 5px;'>Elvis Presley</strong>
                <p style='color: #6B7280; font-size: 0.9em; margin: 0;'>18 músicas #1</p>
            </div>
            <div style='background: white; padding: 15px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s; cursor: pointer;'
                 onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 8px 20px rgba(48,207,208,0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
                <img src='assets/taylor-swift.jpg' 
                     style='width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;'
                     onerror="this.src='https://via.placeholder.com/200x180/30cfd0/ffffff?text=Taylor'"/>
                <strong style='color: #30cfd0; font-size: 1.2em; display: block; margin-bottom: 5px;'>Taylor Swift</strong>
                <p style='color: #6B7280; font-size: 0.9em; margin: 0;'>9 músicas #1</p>
            </div>
            <div style='background: white; padding: 15px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s; cursor: pointer;'
                 onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 8px 20px rgba(168,237,234,0.3)'"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
                <img src='assets/drake.jpg' 
                     style='width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;'
                     onerror="this.src='https://via.placeholder.com/200x180/a8edea/333333?text=Drake'"/>
                <strong style='color: #a8edea; font-size: 1.2em; display: block; margin-bottom: 5px;'>Drake</strong>
                <p style='color: #6B7280; font-size: 0.9em; margin: 0;'>11 músicas #1</p>
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
