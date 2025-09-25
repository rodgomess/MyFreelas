from google import genai
import os, pytz
from dotenv import load_dotenv
from database.supabase_client import SupabaseClient
from datetime import datetime
from time import sleep

from views.helper import load_config
from analysis.helper import extract_decision_proposal_motive

# Inicializando banco de dados
supabase = SupabaseClient()
projects_data = supabase.read_filtered_agent()

# Pegando chave para API Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
agent = genai.Client(api_key=GEMINI_API_KEY)

# Setando data e hora
tz_sp = pytz.timezone("America/Sao_Paulo")

print(f'Total: {len(projects_data)}')

for i in range(len(projects_data)):
    project = projects_data[i]
    config = load_config()

    # Adicionando informações do usuario no prompt e concatenando o projeto atual
    user_info = config['user_info']
    prompt_base = config["prompt"].replace("{user_info}", user_info)
    content = f"{prompt_base} {project}"

    try:
        # Chamando agente
        response = agent.models.generate_content(model="gemini-2.0-flash", contents=content).text

        # Extraindo e atualizando informações da resposta do agente
        decision, proposal, reason_decision = extract_decision_proposal_motive(response)
        project.update({
            "decision": decision,
            "proposal": proposal,
            "reason_decision": reason_decision,
            "updated_at": datetime.now(tz_sp).isoformat()
        })

        # Atualizando no banco de dados
        supabase.update(project, 'link', project['link'])
        sleep(1)

    except Exception as err:
        print(f'Total de projotos analisados: {i}')
        print(f'ERRO: {err}')

print(f"Propostas analisadas: {len(projects_data)}") 