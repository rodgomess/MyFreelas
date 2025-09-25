from playwright.sync_api import sync_playwright
from database.supabase_client import SupabaseClient
import argparse
from time import sleep

from views.helper import load_config

def parse_args():
    parser = argparse.ArgumentParser()
    # Defina tudo num dicionário
    arg_defs = {
        "total_pages": dict(type=int, default=1, help="Total de paginas")
    }
    for name, opts in arg_defs.items():
        parser.add_argument(f"--{name}", **opts)
    
    return parser.parse_args()

supabase = SupabaseClient()

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
    all_projects = []
    URL_FILTERS = load_config()['url_99freelas']
    URL_BASE = 'https://www.99freelas.com.br'
    WEBSITE = "99freelas"

    for page_number in range(total_pages):
        
        url = f'{URL_FILTERS}&page={page_number}'
        page.goto(url)

        projects_list = page.locator('ul.result-list li')
        total_project = projects_list.count()
        
        for i in range(total_project):
            item = projects_list.nth(i)

            # Clicar no botão de aceitar os cookies para nao atrapalhar
            accept_btn = page.locator('#onetrust-accept-btn-handler')
            if accept_btn.is_visible():
                accept_btn.click()

            has_flag = item.evaluate("el => el.classList.contains('with-flag')")
            if not has_flag:
            # Clicar no botão de expandir descrição se ele existir
                btn_expend = item.locator('span.read-more a.more-link')
                if btn_expend.is_visible():
                    btn_expend.click()

                # Pega as informações necessárias
                title = item.locator('h1.title').inner_text()
                link = item.locator('h1.title a').get_attribute("href")
                description = item.locator('div.description').inner_text()

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


    