import sys, subprocess
import streamlit as st
from views.helper import load_config, update_config

def run_agent_analysis():
    cmd = [sys.executable, "-m", 'analysis.agent']
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    # Exibe saída padrão (stdout)
    st.subheader(f"Saída da análise do agente")
    st.code(result.stdout, language="bash")

    # Se houver erros (stderr), exibe também
    if result.stderr:
        st.subheader("Erros do script (stderr)")
        st.code(result.stderr, language="bash")
    if result.returncode == 0:
        st.success("Analisado com sucesso!")
    else:
        st.error(f"Arquivo retornou um erro {result.returncode}")

def run_extract(name, path, total_pages):
    cmd = [sys.executable, "-m", path, "--total_pages", str(total_pages)]
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    # Exibe saída padrão (stdout)
    st.subheader(f"Saída do script {name}")
    st.code(result.stdout, language="bash")

    # Se houver erros (stderr), exibe também
    if result.stderr:
        st.subheader("Erros do script (stderr)")
        st.code(result.stderr, language="bash")
    if result.returncode == 0:
        st.success("Extraido com sucesso!")
    else:
        st.error(f"arquivo.py retornou código de erro {result.returncode}")

def extract_and_analysis(*args):
    st.header("Extração")

    # Opções do forms
    options = {
    "Workana": "extract.extract_workana",
    "99Freelas": "extract.extract_99freelas"
    }
    
    # Check list
    with st.form("form_checklist"):
        st.subheader("Configuração")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.write("Sites para extração (marque pelo menos um):")
            selected = {}
            for key, value in options.items():
                if st.checkbox(key, key=f"chk_{key}"):
                    selected.update({key: value})

        with c2:
             total_pages = st.number_input("Páginas", min_value=1, step=1, value=1, help="Quantidade de páginas que o extrator irá buscar (mínimo 1).", format="%d")
        
        with st.expander("URLs com filtros", expanded=False):
            st.caption("Cole aqui a URL completa do site já com os filtros aplicados.")

            ucol1, ucol2 = st.columns(2)

            with ucol1:
                url_workana = st.text_input(
                    "Workana – URL filtrada",
                    key="url_workana",
                    placeholder="https://www.workana.com/jobs?category=it-programming&language=pt&..."
                )

            with ucol2:
                url_99freelas =st.text_input(
                    "99Freelas – URL filtrada",
                    key="url_99freelas",
                    placeholder="https://www.99freelas.com.br/projects?categoria=programacao&..."
                )

        submitted = st.form_submit_button("Iniciar extração")

    if submitted:

        # Adicionando a URL caso nao seja vazio
        if url_workana != "":
            update_config("url_workana", url_workana)
        if url_99freelas != "":
            update_config("url_99freelas", url_99freelas)

        # Tratando erros do usuario
        if not selected:
            st.error("⚠️ Você precisa marcar pelo menos um site.")
            return
        if total_pages < 1:
            st.error("⚠️ O número de páginas deve ser pelo menos 1.")
            return

        # Executando cada opção marcada
        for name, path in selected.items():
            with st.spinner(f"Executando extração {name} ({total_pages} páginas)..."):
                try:
                    run_extract(name, path, total_pages)
                    pass

                except subprocess.CalledProcessError as e:
                    st.error(f"Erro ao executar arquivo: {e}")
    
    # Analise do agente
    st.header("Analise do Agente")
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = load_config()['user_info']
    user_info = st.text_area("Informações do Usuário", value=st.session_state['user_info'], height=200)

    col1, col2 = st.columns(2)
    # Botão de analise
    with col1:
        if st.button('Salvar informações do usuário'):
            update_config('user_info', user_info)
            st.success('Informações salvas com sucesso')
    
    with col2:
        if st.button('Iniciar análise do agente'):
            with st.spinner(f"Executando análise do agente..."):
                try:
                    run_agent_analysis()

                except subprocess.CalledProcessError as e:
                    st.error(f"Erro ao executar arquivo: {e}")