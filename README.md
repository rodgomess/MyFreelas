# 💼 MyFreelas

Uma plataforma interativa para auxiliar freelancers na busca de projetos em sites de trabalho online, automatizando extração, análise com IA e gerenciamento de propostas em um só lugar.

## 🎯 Objetivo do Projeto

Facilitar o dia a dia de freelancers, permitindo:
- Extração automática de projetos em sites como Workana e 99Freelas.
- Análise com IA (Gemini) para avaliar quais projetos são mais favoráveis, sugerindo propostas personalizadas.
- Gerenciamento prático dos projetos extraídos e analisados, com filtros, histórico e edição de propostas.

## 🖥️ Paginas
### 🔹 1. Extração e Análise
O usuário escolhe o site e o sistema faz o scraping com Playwright, armazena no Supabase e em seguida o Gemini avalia cada projeto, marcando como favorável ou não e sugerindo propostas personalizadas automáticas.

Funcionalidades:
- Quantas páginas extrair.
- Pode configurar a URL com filtros personalizados.
- Usuario pode alterar suas experiências a qualquer momento
- Explica o motivo da decisão.

📸 Demonstração – Extração e Análise
<video src="https://github.com/user-attachments/assets/e8139265-20d4-43f9-b8e7-f670a5f86871" controls width="800"></video>

### 🔹 2. Escolher Propostas
Após a análise, o usuário pode navegar, filtrar, ajustar as propostas geradas e decidir se aceita ou recusa cada projeto.

Funcionalidades:
- Tags informando projetos favoráveis e escolhidos pelo usuário.
- Interface para navegar nos projetos extraídos e analisados.
- Possibilidade de filtrar projetos favoráveis e selecionados
- Permite editar e ajustar a proposta sugerida pelo agente Gemini.
- Link direto para o projeto no site original.
- Botões para Aceitar ou Recusar propostas, salvando a decisão no banco.

📸 Demonstração – Escolher Propostas
<video src="https://github.com/user-attachments/assets/571907b8-deba-4efd-9ec5-8a716e847208" controls width="800"></video>

### 🔹 3. Consultar Banco de Dados
Permite visualizar todos os projetos salvos em tabela com filtros avançados (palavra-chave, decisões, datas, site) e excluir dados em lote com segurança.

Funcionalidades:
Visualização tabular de todos os projetos armazenados.
Filtros avançados:

- Texto (título, descrição, proposta)
    - Decisão do agente
    - Decisão do usuário
    - Site de origem
    - Intervalo de datas
    - Apenas registros sem proposta
- Possibilidade de apagar registros por faixa de data com confirmação (ação irreversível).

📸 Demonstração – Consultar Banco de Dados
<video src="https://github.com/user-attachments/assets/2ca7852e-7855-4229-bc7d-e82dfd122b9a" controls width="800"></video>



⚙️ Tecnologias Utilizadas

- Frontend: Streamlit + CSS customizado
- Web Scraping: Playwright
- Banco de Dados: Supabase
- IA: Google Gemini API
- Backend auxiliar: Python (subprocess, argparse, requests)

## 🧑‍💻 Autor
Rodrigo Gomes
🔗 [LinkedIn](https://www.linkedin.com/in/rodrigogomes-profile/)
