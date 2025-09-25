import streamlit as st
from streamlit_option_menu import option_menu

from database.supabase_client import SupabaseClient
from views.show_table import show_table
from views.extract_and_analysis import extract_and_analysis
from views.select_project_page import select_project_page

from views.helper import load_css

st.set_page_config(layout="wide")
load_css(st, "views/styles.css")

supabase = SupabaseClient()

# Rotas existentes
ROUTES = {
    "Escolher Propostas": select_project_page,
    "Consultar Banco de Dados": show_table,
    "Extração e Análise": extract_and_analysis,
}

# Inicializa a variavel rota 
if "route" not in st.session_state:
    st.session_state["route"] = "Escolher Propostas"

# Side bar contendo todas as views
with st.sidebar:

    selected = option_menu(
        "Navegação",
        list(ROUTES.keys()),
        icons=["list-task", "database", "gear"],
        menu_icon="cast",
        default_index=list(ROUTES.keys()).index(st.session_state["route"]),
        styles={
            "container": {"padding": "0px", "width": "350px"},
            "nav-link": {"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"},
        },
        key="nav_menu",
    )

    # Rodapé fixo no final da sidebar
    st.markdown(
        """
        <div style='position: absolute; bottom: 25px; width: 100%; text-align: center;
                    font-size: 13px; color: gray;'>
            Desenvolvido por <a href='https://github.com/rodgomess' target='_blank' style='color: #888;'>@rodgomess</a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.session_state["route"] = selected
# Renderiza a view corrente
ROUTES[selected](supabase)