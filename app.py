import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from database import SupabaseClient
from dotenv import load_dotenv
import pandas as pd
import os, pytz
from datetime import datetime
from functools import partial

st.set_page_config(layout="wide")

def select_project():
    def display_text(text):
        return st.markdown(f"""
        <div style="
            border: 1px solid #0a0a0a;
            padding: 16px;
            border-radius: 8px;
            background-color: #363636;
            margin-bottom: 10px;
        ">
            <p style="margin: 0;">
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    def next_proj():
        if st.session_state.idx < len(st.session_state.projects_data) - 1:
            st.session_state.idx += 1

    def prev_proj():
        if st.session_state.idx > 0:
            st.session_state.idx -= 1

    def load_projects(reader_fn):
        st.session_state.idx = 0
        idx = st.session_state.idx
        st.session_state.projects_data = reader_fn()

    tz_sp = pytz.timezone("America/Sao_Paulo")
    load_all = partial(load_projects, supabase.read)
    load_fav = partial(load_projects, supabase.read_filtered_favorable)
    load_accepted = partial(load_projects, supabase.read_filtered_accepted)

    if "projects_data" not in st.session_state:
        st.session_state["projects_data"] = supabase.read()
    
    st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            height: 3em;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .tag-green {
        display: inline-block;
        background-color: #e6f4ea;
        color: #2e7d32;
        border: 1px solid #2e7d32;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.9rem;
        vertical-align: middle;
        margin-left: 10px; /* espaço entre título e tag */
    }

    .tag-red {
        display: inline-block;
        background-color: #fdecea;    /* fundo levemente avermelhado */
        color: #c62828;               /* texto vermelho escuro */
        border: 1px solid #c62828;    /* borda vermelha */
        border-radius: 4px;           /* cantos arredondados */
        padding: 2px 8px;             /* espaçamento interno */
        font-size: 0.9rem;            /* tamanho de fonte ajustável */
        vertical-align: middle;       /* alinha com texto ao redor */
    }

    .tag-unselected {
        display: inline-block;
        background-color: #fdecea;    /* fundo levemente avermelhado */
        color: #c62828;               /* texto vermelho escuro */
        border: 1px solid #c62828;    /* borda vermelha */
        border-radius: 4px;           /* cantos arredondados */
        padding: 2px 8px;             /* espaçamento interno */
        font-size: 0.9rem;            /* tamanho de fonte ajustável */
        vertical-align: middle;       /* alinha com texto ao redor */
    }

    .tag-selected {
        display: inline-block;
        background-color: #e6f4ea;    /* fundo levemente esverdeado */
        color: #2e7d32;               /* texto verde escuro */
        border: 1px solid #2e7d32;    /* borda verde */
        border-radius: 4px;           /* cantos arredondados */
        padding: 2px 8px;             /* espaçamento interno */
        font-size: 0.9rem;            /* tamanho de fonte ajustável */
        vertical-align: middle;       /* alinha com texto ao redor */
    }

    .tag-neutral {
        display: inline-block;
        background-color: #f5f5f5;    /* fundo cinza claro */
        color: #616161;               /* texto cinza escuro */
        border: 1px solid #bdbdbd;    /* borda cinza média */
        border-radius: 4px;           /* cantos arredondados */
        padding: 2px 8px;             /* espaçamento interno */
        font-size: 0.9rem;            /* tamanho de fonte ajustável */
        vertical-align: middle;       /* alinha com texto ao redor */
    }
    
    .tag-green, .tag-red, .tag-neutral, .tag-selected, .tag-unselected {
        white-space: nowrap;       /* não permite quebras */
        margin: 0px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    if "idx" not in st.session_state:
        st.session_state["idx"] = 0
    idx = st.session_state.idx
    
    col_prev, col_main, col_filters = st.columns([3, 10, 4])

    with col_filters:
        st.text('Filtros:')
        st.button("Todos", on_click=load_all)
        st.button("Favoráveis", on_click=load_fav)
        st.button("Selecionados", on_click=load_accepted)

    project = st.session_state.projects_data[idx]
    with col_prev:
        st.button("⇽", on_click=prev_proj)
                
        st.button("⇾", on_click=next_proj)
        
        display_text(f'Total: {idx+1}/{len(st.session_state.projects_data)}')

        if st.button("Link do Projeto"):
            components.html(
                f"<script>window.open('{project['link']}', '_blank');</script>",
                height=0,
                width=0
            )

    with col_main:

        tags = []
        if project['decision'] == "favoravel":
            tags.append(("Favorável", "tag-green"))
        else:
            tags.append(("Não Favorável", "tag-red"))

        ud = project.get('user_decision')
        if ud == "ACCEPTED":
            tags.append(("Selecionada", "tag-selected"))
        elif ud == "DENIED":
            tags.append(("Não Selecionada", "tag-unselected"))
        else:
            tags.append(("Sem Decisão", "tag-neutral"))

        # 2) Cria colunas: a primeira larga pro título, e uma para cada tag
        col_weights = [8] + [8] * len(tags)
        cols = st.columns(col_weights)

        # 3) Renderiza
        cols[0].text("Título")
        for i, (label, css_class) in enumerate(tags, start=1):
            cols[i].markdown(f'<span class="{css_class}">{label}</span>', unsafe_allow_html=True)

        display_text(project["title"])

        st.text("Motivo da Decisão")
        display_text(project["reason_decision"])

        st.text("Descrição")
        display_text(project["description"])

        default_text = project.get("proposal") or ""
        st.session_state["proposal_text_area"] = default_text

        # 2) Chama o textarea sem value, só com a key
        proposal = st.text_area("Proposta", key="proposal_text_area", height=200)


        col1, col2 = st.columns(2)
        with col1:
            if st.button("Aceitar", key="accept"):
                if idx < len(st.session_state.projects_data) - 1:
                    st.session_state.idx = idx + 1
                    supabase.update({
                        "link": project['link'],
                        "user_decision": "ACCEPTED",
                        "proposal": proposal,
                        "updated_at": datetime.now(tz_sp).isoformat()
                    }, 'link', project["link"])

        with col2:
            if st.button("Recusar", key="reject"):
                if idx < len(st.session_state.projects_data) - 1:
                    st.session_state.idx = idx + 1
                    supabase.update({
                        "link": project['link'],
                        "user_decision": "DENIED",
                        "updated_at": datetime.now(tz_sp).isoformat()
                    }, 'link', project["link"])

def show_table():
    # st.set_page_config(layout="wide")

    pd_projects = pd.DataFrame(supabase.read())

    st.dataframe(pd_projects, width=5000, height=600)

# Exemplo de dados; substitua pela sua lista/lê do banco
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        min-width: 400px !important;
        max-width: 400px !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    selected = option_menu(
        menu_title="Navegação",
        options=["Escolher Propostas", "Consultar Banco de Dados", "Configuração e Extração"],
        icons=["list-task", "database", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0px", "width": "350px"},
            "nav-link": {"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}
        }
    )

if selected == "Escolher Propostas":
    select_project()
elif selected == "Consultar Banco de Dados":
    show_table()
else:
    st.header("Página: Configuração e Extração")