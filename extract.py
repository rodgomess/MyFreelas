from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from database import SupabaseClient

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)

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
    browser = p.chromium.launch(headless=True)

    context = browser.new_context()
    page = context.new_page()

    total_page = 11
    all_projects = []

    for page_number in range(total_page):
        URL_BASE = 'https://www.99freelas.com.br'
        url = f'{URL_BASE}/projects?order=mais-recentes&categoria=web-mobile-e-software&page={page_number}'
        page.goto(url)

        projects_list = page.locator('ul.result-list li')
        total_project = projects_list.count()
        
        for i in range(total_project):
            item = projects_list.nth(i)

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
                    "link": URL_BASE+link,
                })
    browser.close()
    

    all_projects = remove_duplicate(all_projects)
    if len(all_projects) > 1:
        supabase.upsert(all_projects)

    print(f"TOTAL DE PROJETOS ARMAZENADOS: {len(all_projects)}")