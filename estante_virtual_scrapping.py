import re
import csv
import numpy as np
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

#instancia-se um array aonde serão armezanada informações  dos livros
livros_para_comprar = []

#pega um csv com os links dos livros para realizar o scraping
links = pd.read_csv('./links_para_livros.csv')

for index, rows in links.iterrows():
    if index == 5:
        break

    dic_livro = {}

    #Realiza um request que vai para página dos livros com interesse de compra
    url = 'https://www.estantevirtual.com.br/{}'.format(links['link'][index])
    response = rq.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    #  Na parte geral do código decidi que seguiria a mesma ordem presente no source-code da página, assim como
    #também criaria uma variavel com mesmo nome da tag presente no código fonte para ficar mais fácil de se guiar
    #drante o desenvolvimento, a var article é primeira parte que me interessa dentro da página que contem as principais
    #informações do livro como titulo do livro e autor do mesmo que são as primeiras informações que busco,
    #dito isso eu busco primeiro a tag <article>, assim consigo pegar o seus primeiros filhos que são necessários que é
    #h1 e h2 presente no código a baixo
    article = html.find('article', {'class': 'row livro-exemplar link-back'})
    dic_livro['Nome do Livro'] = article.find('h1', {'class': 'livro-titulo col-12'}).get_text().strip()
    autor_nome = article.find('h2', {'class': 'livro-autor col-12'})
    dic_livro['Autor do Livro'] = autor_nome.find('span').get_text()


    div_preço = html.find('div', {'class': 'col-4 info-livro-vendedor-aside'})
    dic_livro['Valor'] = div_preço.find_all('strong', {'class': 'livro-preco-valor'})[0].get_text().strip()
    dic_livro['Frete'] = div_preço.find_all('span', {'class': 'livro-preco-frete'})[0].get_text().strip().strip('+ envio*')

    #   a tag <section> contém informações importantes do livro, como a condição (no site se apresenta como tipo),
    #a editora, o idioma, ano de públicação, ISBN, também a descrição que normalmente é composta por uma descrição da
    #da condição do livro do livro, busquei usando o find_all em 4 seções, pois só assim conseguia encontrar as
    #informações desejadas
    section = html.find('section', {'class': 'col-6 m-info'})
    dic_livro['Condição'] = section.find_all('p')[0].get_text().strip().strip('Tipo:').strip()
    dic_livro['Editora/Publicação'] = section.find_all('p')[1].get_text().strip('Editora:\n\n')
    dic_livro['Ano de publicação'] = section.find('p', {'class': 'livro-specs info-year'}).get_text().strip().strip('Ano:').strip()
    dic_livro['ISBN'] = section.find_all('p')[5].get_text().strip().strip('ISBN:').strip()
    dic_livro['Idioma'] = section.find_all('p')[6].get_text().strip().strip('Idioma:').strip()
    dic_livro['Descricao da condição'] = section.findAll('span', {'itemprop': 'description'})[0].get_text().strip().strip().strip()

    # A tag <aside> contém as informações laterais sobre o vendedor, como o nome do sebo, e reviews dos usuários sobre o sebo
    aside = html.find('aside', {'class': 'sobre-o-livreiro'})
    dic_livro['Loja'] = [a['href'] for a in html.select('a[href]')][100:101]
    dic_livro['Reviews da Loja'] = aside.find_all('div', {'class': 'seller-review-box'})[0].get_text()

    #Pega itens atual do dicionário e adicona a lista
    livros_para_comprar.append(dic_livro)

#Transforma o meu array em um DataFrame com auxilio do pandas
livros = pd.DataFrame(livros_para_comprar)

#Pega o meu DataFrame e converte em arquivo csv
livros.to_csv('livros_para_comprar.csv', index=False)

print(livros)

for livro in livros_para_comprar:
    print(livro)