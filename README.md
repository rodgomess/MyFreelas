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

📸 GIF – Extração e Análise
![20250926-0002-14 5360566](https://github.com/user-attachments/assets/9002009e-1845-4b43-82fc-5dfbde4e3e47)

### 🔹 2. Escolher Propostas
Após a análise, o usuário pode navegar, filtrar, ajustar as propostas geradas e decidir se aceita ou recusa cada projeto.

Funcionalidades:
- Interface para navegar nos projetos extraídos e analisados.
- Possibilidade de filtrar projetos favoráveis e selecionados
- Permite editar e ajustar a proposta sugerida pelo agente Gemini.
- Link direto para o projeto no site original.
- Botões para Aceitar ou Recusar propostas, salvando a decisão no banco.

📸 GIF – Escolher Propostas
![Vídeo sem título ‐ Feito com o Clipchamp](https://github.com/user-attachments/assets/42b80238-466c-4267-b571-a584f357cb44)


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

📸 GIF – Consultar Banco de Dados
![Vídeo sem título ‐ Feito com o Clipchamp (1)](https://github.com/user-attachments/assets/c3e54bc0-109a-4567-86ad-e5a451621634)


⚙️ Tecnologias Utilizadas

- Frontend: Streamlit + CSS customizado
- Web Scraping: Playwright
- Banco de Dados: Supabase
- IA: Google Gemini API
- Backend auxiliar: Python (subprocess, argparse, requests)

## 🧑‍💻 Autor
Rodrigo Gomes
🔗 [LinkedIn](https://www.linkedin.com/in/rodrigogomes-profile/)
