from playwright.sync_api import sync_playwright
from database.supabase_client import SupabaseClient
import argparse

from views.helper import load_config

supabase = SupabaseClient()

def parse_args():
    parser = argparse.ArgumentParser()
    # Defina tudo num dicionário
    arg_defs = {
        "total_pages": dict(type=int, default=1, help="Total de paginas")
    }

    for name, opts in arg_defs.items():
        parser.add_argument(f"--{name}", **opts)
    
    return parser.parse_args()

def remove_duplicate(list_dicts):
    vistos = set()
    resultado = []
    for item in list_dicts:
        link = item.get('link')
        if link not in vistos:
            vistos.add(link)
            resultado.append(item)
    return resultado

with sync_playwright() as p:
    args = parse_args()

    browser = p.chromium.launch(headless=True)

    context = browser.new_context()
    page = context.new_page()

    total_pages = args.total_pages
    URL_FILTERS = load_config()['url_workana']
    URL_BASE = 'https://www.workana.com'
    WEBSITE = "Workana"

    all_projects = []

    for page_number in range(total_pages):
        
        url = f'{URL_FILTERS}&page={page_number}'
        page.goto(url)

        # Clicar no botão de aceitar os cookies para nao atrapalhar se existir
        try:
            page.locator('#onetrust-accept-btn-handler').click(timeout=2000)  # espera até 2s
        except:
            pass

        projects_list = page.locator("#projects .project-item")
        total_project = projects_list.count()
        
        for i in range(total_project):
            item = projects_list.nth(i)

            # Clica no botão de ver mais detalhes
            btn_expend = item.get_by_text('Ver mais detalhes', exact=True)
            if btn_expend.is_visible():
                btn_expend.click()
            
            # Pega as informações necessárias
            title = item.locator('h2.project-title').inner_text()
            link = item.locator('h2.project-title span a').get_attribute("href")
            description = item.locator('div.project-details').inner_text()

            all_projects.append({
                "title": title,
                "description": description,
                "website": WEBSITE,
                "link": URL_BASE+link,
            })
    browser.close()

    all_projects = remove_duplicate(all_projects)
    if len(all_projects) > 1:
        supabase.upsert(all_projects)

    print(f"TOTAL DE PROJETOS ARMAZENADOS: {len(all_projects)}")