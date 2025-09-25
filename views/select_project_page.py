from datetime import datetime
from functools import partial
import pytz
from views.helper import display_text
import streamlit.components.v1 as components
import streamlit as st

def select_project_page(supabase):
    # Avança para a proxima proposta
    def next_proj():
        if st.session_state.idx < len(st.session_state.projects_data) - 1:
            st.session_state.idx += 1

    # Volta uma proposta
    def prev_proj():
        if st.session_state.idx > 0:
            st.session_state.idx -= 1

    # Atualiza na base a decisão o usuario
    def take_decision(decision):
        p = st.session_state.projects_data[st.session_state.idx]
        
        supabase.update({
            "link": p['link'],
            "user_decision": decision,
            "proposal": st.session_state[proposal_key],
            "updated_at": datetime.now(tz_sp).isoformat()
        }, 'link', p["link"])

        # Avaça para a proxima proposta
        next_proj()

    # Carrega os projetos de acordo com o filtro
    def load_projects(reader_fn):
        st.session_state.idx = 0
        st.session_state.projects_data = reader_fn()

    tz_sp = pytz.timezone("America/Sao_Paulo")

    # Funções ajustadas para usar no button
    load_all = partial(load_projects, supabase.read_to_front)
    load_fav = partial(load_projects, supabase.read_filtered_favorable)
    load_accepted = partial(load_projects, supabase.read_filtered_accepted)
    project_accepted = partial(take_decision, 'ACCEPTED')
    project_denied = partial(take_decision, 'DENIED')

    # Inicializano variaveis
    if "projects_data" not in st.session_state:
        st.session_state["projects_data"] = supabase.read()
    if "idx" not in st.session_state:
        st.session_state["idx"] = 0
    
    col_prev, col_main, col_filters = st.columns([3, 10, 4])

    # Filtros lateral
    with col_filters:
        st.text('Filtros:')
        st.button("Todos", on_click=load_all)
        st.button("Favoráveis", on_click=load_fav)
        st.button("Selecionados", on_click=load_accepted)

    # Quando ano existir projetos aparece uma mensagem
    if len(st.session_state.projects_data) == 0:
        display_text('Nenhum projeto encontrado')
        return

    # Instanciando projeto atual
    project = st.session_state.projects_data[st.session_state.idx]

    # Botão de avançar e voltar
    with col_prev:
        st.button("⇽", key="prev-button", on_click=prev_proj)
        st.button("⇾", key="next-button", on_click=next_proj)
        
        # Mostra a posição na fila
        display_text(f'Propostas: {st.session_state.idx+1}/{len(st.session_state.projects_data)}')

        # Botão com link do projeto
        print(project['link'])
        st.button("Link do Projeto", on_click=lambda: components.html(f"<script>window.open('{project['link']}', '_blank');</script>"))
            

    with col_main:
        # Tags
        # Mapeamento da decisão do agente
        decision_map = {
            "favoravel": ("Favorável", "tag-green"),
            "nao_favoravel": ("Não Favorável", "tag-red")
        }
        tag_fav = decision_map.get(project["decision"], ("Não Favorável", "tag-red"))

        # Mapeamento da decisão do usuário
        user_decision_map = {
            "ACCEPTED": ("Selecionada", "tag-selected"),
            "DENIED": ("Não Selecionada", "tag-unselected"),
            None: ("Sem Decisão", "tag-neutral")
        }
        tag_user_decision = user_decision_map.get(project.get("user_decision"), ("Sem Decisão", "tag-neutral"))

        # Cria tags
        st.markdown(f"""
            <div class="div-tags">
                <span class="title">Título</span>
                <div>
                    <span class="{tag_fav[1]}">{tag_fav[0]}</span>
                    <span class="{tag_user_decision[1]}">{tag_user_decision[0]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Titulo
        display_text(project["title"])

        # Motivo da decisão
        st.text("Motivo da Decisão")
        display_text(project["reason_decision"])

        # Decrição
        st.text("Descrição")
        display_text(project["description"])

        # Adiciona a proposta criada pelo agente no texto
        proposal_key = f"proposal_{project['link']}"
        if proposal_key not in st.session_state:
            st.session_state[proposal_key] = project.get("proposal") or ""
        st.text_area("Proposta", key=proposal_key, height=200)
        
        # Botões de aceitar e recusar
        col1, col2 = st.columns(2)
        with col1:
            st.button("Aceitar", key="accepted", on_click=project_accepted)
        with col2:
            st.button("Recusar", key="denied", on_click=project_denied)