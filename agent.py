from google import genai
import json, os, re
from dotenv import load_dotenv
from database import SupabaseClient
from datetime import datetime
from time import sleep
import pytz

def extract_decision_proposal_motive(text):
    # 1) Decisão
    decision = next(
        (line.split(":", 1)[1].strip().lower()
         for line in text.splitlines()
         if line.lower().startswith("decisão:")),
        None
    )

    proposal = None
    # 2) Proposta só se favorável
    if decision == "favoravel":
        m = re.search(
            r"^Proposta:\s*(.*?)(?=^Motivo da decisão:|\Z)",
            text,
            flags=re.DOTALL | re.MULTILINE
        )
        if m:
            proposal = m.group(1).strip()

    # 3) Motivo da decisão
    motive = None
    m2 = re.search(r"^Motivo da decisão:\s*(.*)$", text, flags=re.MULTILINE|re.DOTALL)
    if m2:
        motive = m2.group(1).strip()

    return decision, proposal, motive



load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
projects_data = supabase.read_filtered_agent()

agent = genai.Client(api_key=GEMINI_API_KEY)

tz_sp = pytz.timezone("America/Sao_Paulo")
print(f'Total: {len(projects_data)}')
for i in range(len(projects_data)):
    project = projects_data[i]
    
    content = f"""
    Você é um assistente especializado em avaliação de projetos freelas e geração de propostas. Recebe:

    1. Um objeto contendo o projeto, onde cada objeto tem os campos:
    - "title": título do projeto
    - "link": URL do projeto
    - "description": descrição completa do projeto

    2. As informações do usuário:
        nome do usuario: "Rodrigo Gomes
        ferramentas: Playwright, Python, Pandas, PySpark, web scrapping, criação de bot para whatsapp e telegram, twilio, Agente IA, streamlit
        experiencias: Trabalho a 5 anos como engenheiro de dados, fazendo processos ETL para Ambev, para projetos paralelos ja fiz integrações de chat bot humanizado com intuito de anotar pedidos de um resturante, ja fiz processos de scrapping de sites de vagas de emprego

    Sua tarefa, para cada projeto:

    1. Avaliar se o projeto é favorável para ser feito pelo usuario, considerando que um projeto é favorável se:
    - A descrição cita pelo menos uma das tecnologias ou ferramentas em que o usuario tem experiência ou cita algo parecido com as tecnologias que o usuario tem experiencia.
    - As tarefas descritas são compatíveis com o perfil do usuario.
    - A solução para o projeto envolve ferramentas que o usuario tem experiencia.

    2. Para cada projeto:
    - **Se for favorável**: gere um texto de proposta que o usuario possa enviar ao cliente. A proposta deve conter:
        - Saudação cordial
        - Breve apresentação
        - Conexão direta com o projeto (“Vejo que vocês precisam de … e posso ajudar com …”)
        - Faça uma breve estruturação de esboço do projeto
        - Chamada para ação (“Fico à disposição para conversar nos detalhes e iniciar o trabalho.”)
    - **Se não for favorável**: responda apenas:
        ```
        projeto não favoravel
        ```
    - Escreva o motivo da decisão
    **Formato de saída**:
    Para cada projeto, comece com:
    Título: <title>
    Decisão: <“Favoravel” ou “Não favoravel”>
    - Se “Favoravel”, logo abaixo insira Proposta: <proposta>.  
    - Se “Não favoravel”, logo abaixo insira Proposta: e só coloque “Projeto nao favoravel”.
    Motivo da decisão: <Motivo da decisão>

    Segue abaixo o projeto
    {project}
    """
    
    response = agent.models.generate_content(model="gemini-2.0-flash", contents=content).text

    decision, proposal, reason_decision = extract_decision_proposal_motive(response)

    project.update({
        "decision": decision,
        "proposal": proposal,
        "reason_decision": reason_decision,
        "updated_at": datetime.now(tz_sp).isoformat()
    })

    supabase.update(project, 'link', project['link'])
    
    print(f"Propostas analisdas: {i}")

    sleep(1)