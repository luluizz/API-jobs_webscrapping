from fastapi import FastAPI, Response
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import geopandas as gpd
import geobr
import matplotlib.pyplot as plt
import unidecode
import json
from fastapi.openapi.utils import get_openapi
pd.set_option('display.max_rows', None)
vagas_todas = {}
site = []

app = FastAPI()

if __name__ == "__main__":  
    import uvicorn 
    uvicorn.run(app, host="localhost", port=8000)
    
@app.get("/")
def pegar_local(sigla_estado: str, cidade:str):
    sigla_estado = sigla_estado.upper()
    nome_estado_original = geobr.read_state(code_state=f'{sigla_estado}')[f'name_state'].to_string(index=False)
    todos_muni = geobr.read_municipality(code_muni=f"{sigla_estado}", year=2020)
    nome_muni_original = todos_muni['name_muni'].to_string(index=False)
    nome_muni = unidecode.unidecode(nome_muni_original).lower()
    cidade = unidecode.unidecode(cidade).lower()
    sigla_estado = sigla_estado.lower()
    pesquisa_muni = re.search(cidade, nome_muni)
    if pesquisa_muni != None:
        nome_cidade_original = nome_muni_original[pesquisa_muni.start():pesquisa_muni.end()]
        nome_cidade = cidade
        nome_cidade_separado = cidade.replace(' ', '-')
        infojobs(nome_cidade_separado, sigla_estado)
        linkedin(nome_cidade_original, nome_estado_original)
        vagas(nome_cidade, sigla_estado)
        return {"vagas:":resultado(site, vagas_todas)}
    else:
        return "Sua cidade não foi encontrada, tente  novamente!"
    
def infojobs(nome_cidade_separado: str, sigla_estado: str):
    url_infojobs = f'https://www.infojobs.com.br/empregos-em-{nome_cidade_separado},-{sigla_estado}.aspx'
    html_infojobs = requests.get(url_infojobs)
    soup_infojobs = BeautifulSoup(html_infojobs.text, 'html.parser')
    scrapping_infojobs = soup_infojobs.find_all("div", attrs={"class": "card card-shadow card-shadow-hover text-break mb-16 grid-row js_rowCard active"})
    scrapping_infojobs.extend(soup_infojobs.find_all("div", attrs={"class": "card card-shadow card-shadow-hover text-break mb-16 grid-row js_rowCard"}))
    titulo_infojobs = []
    contratante_infojobs = []
    local_infojobs = []
    for vaga_infojobs in scrapping_infojobs:
        titulo_infojobs.append(vaga_infojobs.a.h2.text.strip()) #titulo da vaga
        contratante_infojobs.append(vaga_infojobs.find("div", attrs={"class":"text-body"}).text.strip()) #nome da empresa ou contratante
        local_infojobs.append(vaga_infojobs.find("div", attrs={"class":"small text-medium mr-24"}).text.split(",")[0].strip()) #cidade do local da vaga
        site.append("infojobs")
    vagas_todas["titulo"] = titulo_infojobs
    vagas_todas["empresa"] = contratante_infojobs
    vagas_todas["local"] = local_infojobs
    vagas_todas["site"] = site

def linkedin(nome_cidade_original: str, nome_estado_original: str):
    url_linkedin = f'https://www.linkedin.com/jobs/search/?location={nome_cidade_original}-{nome_estado_original}'
    html_linkedin = requests.get(url_linkedin)
    soup_linkedin = BeautifulSoup(html_linkedin.text, 'html.parser')
    scrapping_linkedin = soup_linkedin.find_all("div", attrs={"class":"base-search-card__info"})
    titulo_linkedin = []
    contratante_linkedin = []
    local_linkedin = []
    for vaga_linkedin in scrapping_linkedin:
        titulo_linkedin.append(vaga_linkedin.h3.text.strip().replace("\n", " ")) #titulo da vaga
        contratante_linkedin.append(vaga_linkedin.h4.text.strip()) #contratante
        local_linkedin.append(vaga_linkedin.div.span.text.strip())#local
        site.append("linkedin")
    vagas_todas["titulo"].extend(titulo_linkedin)
    vagas_todas["empresa"].extend(contratante_linkedin)
    vagas_todas["local"].extend(local_linkedin)

def vagas(nome_cidade: str, sigla_estado: str):
    url_vagas = f'https://www.vagas.com.br/vagas-em-{nome_cidade}-{sigla_estado}'
    html_vagas = requests.get(url_vagas)
    soup_vagas = BeautifulSoup(html_vagas.text, 'html.parser')
    scrapping_vagas = soup_vagas.find_all("li", attrs={"class":"vaga odd"})
    scrapping_vagas.extend(soup_vagas.find_all("li", attrs={"class":"vaga even"}))
    titulo_vagas = []
    contratante_vagas = []
    local_vagas = []
    for vaga_vagas in scrapping_vagas:
        titulo_vagas.append(vaga_vagas.find("a", attrs={"class":"link-detalhes-vaga"}).text.strip()) #titulo
        contratante_vagas.append(vaga_vagas.find("span", attrs={"class":"emprVaga"}).text.strip()) #contratante
        local_vagas.append(vaga_vagas.find("span", attrs={"class":"vaga-local"}).text.strip()) #local
        site.append("vagas.com")
    vagas_todas["titulo"].extend(titulo_vagas)
    vagas_todas["empresa"].extend(contratante_vagas)
    vagas_todas["local"].extend(local_vagas)

def resultado(site, vagas_todas):
    vagas_todas["site"] = site
    vagas_todas_df = pd.DataFrame(vagas_todas)
    return vagas_todas_df.T
    
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
