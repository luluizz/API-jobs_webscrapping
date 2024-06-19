# API-jobs_webscrapping

## Para que serve?
É uma API com webscrapping de busca de empregos em três dos maiores sites de anúncios de vagas do Brasil, o Infojobs, o Linkedin e o Vagas.com.


## Como usar?
### Ambiente Virtual
É sugerido criar um [ambiente virtual](https://www.treinaweb.com.br/blog/criando-ambientes-virtuais-para-projetos-python-com-o-virtualenv) para esse projeto.

Depois de criar e ativar o ambiente virtual execute [requirements.txt](https://medium.com/pyladiesbh/requirements-em-python-ec88b42058a6) para instalar as bibliotecas nececssárias.

### Executar a API
No terminal, com o ambiente virtual ativado, digite o seguinte comando:
```sh
uvicorn main:app
```
Em seguida o terminal irá retornar o endereço onde a API está rodando, assim como na foto abaixo:
![image](https://github.com/luluizz/API-jobs_webscrapping/assets/118929650/464a1eaf-28a2-4213-9a87-246c23d98c20)

Coloque o endereço na barra de pesquisa do seu navegador e aperte enter.

### Testar a API

Para testar digite no endereço da API "/docs" e aperte enter.

![image](https://github.com/luluizz/API-jobs_webscrapping/assets/118929650/694e782b-62fa-4d75-a8b8-b41297ad243d)

Clique em "GET/ pegar_local" e depois em "Try it out".
![image](https://github.com/luluizz/API-jobs_webscrapping/assets/118929650/e70be834-be2b-4ed1-a1c1-88606e3ada2f)

Digite a sigla do estado que deseja pesquisar e o nome da cidade.
![image](https://github.com/luluizz/API-jobs_webscrapping/assets/118929650/02db6719-a1d8-4534-9228-37a89d6f76d1)

Em response body estará seu resultado.
![image](https://github.com/luluizz/API-jobs_webscrapping/assets/118929650/3ed9beb8-67d9-41cc-a016-e3f2c7f6b734)
