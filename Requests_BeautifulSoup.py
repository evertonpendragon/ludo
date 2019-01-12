import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

#abre a pagina
#r = urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
page = requests.get('https://www.ludopedia.com.br/jogo/kory')

#se a página foi baixada com sucesso = 200
print(page.status_code)

#elementos da página
#list(soup.children)


#exibe conteúdo da página
#page.content

#texto da pag
data = page.text


soup = BeautifulSoup(data, 'html.parser')



#encontra os links
#for link in soup.find_all('a'):
    #print(link.get('href'))

########################################################################################################################
#titulo
titulo = soup.find('div', class_="jogo-top-main")
titulo =  titulo.find('a', href="#").text.strip()
#print(titulo)

#ano
ano = soup.find('div', class_="jogo-top-main")
ano =  ano.find('span', class_=" text-xs").text.strip()
print(titulo, ano)

# Rank
# for div in soup.find_all('div', class_="jogo-top-capa"):
rank = []
item = soup.find('div', class_="mar-top hidden-xs")
for x in item.find_all(class_="block"):
    # print(x.contents)
    # isso tbm funciona, mas é mais trabalhodo->#print(x.contents[0],x.contents[1].find('a').contents[0]) ## ['Rank: ', <span><u><a class="text-bold" href="https://www.ludopedia.com.br/search_jogo">25</a></u></span>]
    rank.append({x.contents[0].replace(': ', ''): x.contents[
        1].text.strip()})  ## ['Rank: ', <span><u><a class="text-bold" href="https://www.ludopedia.com.br/search_jogo">25</a></u></span>]
print(rank)
# Tenho, quero, tive, favorito
listaDesejos = []
for div in soup.find_all(class_="btn-colecao"):
    for item in list(div):
        colecao, qtd = (item.split())
        qtd = ''.join([numero for numero in qtd if numero.isdigit()])
        listaDesejos.append({colecao: qtd})
print(listaDesejos)

##Tenho, quero, tive, favorito
#for div in soup.find_all(class_="btn-colecao"):
#    for item in  list(div):
#        print(item)

# mercado
anuncios = []
blkAnuncio = soup.find(id="bloco-anuncios-sm")

linkAnuncio = blkAnuncio.find('div', class_="btn-group")
linkAnuncio = (linkAnuncio.find('a')['href'])

pgAnuncio = requests.get(linkAnuncio)
pgAnuncio = BeautifulSoup(pgAnuncio.text, 'html.parser')

blkAnuncio = pgAnuncio.find('div', id="anuncios")
# print(blkAnuncio)
if blkAnuncio != None:
    for table in blkAnuncio.findAll('table'):
        rows = table.find_all('tr')
        for row in rows:
            # print("row: " , type(row))
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            anuncios.append([ele for ele in cols])  # Get rid of empty values
    qtdAnuncios = {"Anuncios": len(anuncios) - 1}
else:
    qtdAnuncios = {"Anúncios": 0}
print(qtdAnuncios)
print(anuncios)
registro = [titulo, ano, rank, listaDesejos, qtdAnuncios, anuncios]

print(registro)

arq = open('C:/Users/Everton/Desktop/ludopedia.txt', 'a', encoding="utf-8")
arq.write(str(registro)+"\n")
arq.close()

#for row in table.findAll("tr"):
        #    cells = row.findAll("td")
        #    print(cells[0].get_text())

#for table in soup.find_all(class_="table"):
#    for row in table.findAll("tr"):
#        cells = row.findAll("td")
#        print(cells)
#


'''
for div in soup.find_all('div'):

    try:
        #print(div)
        div2 = BeautifulSoup(div, 'html.parser')
        for but in div2.find_all('button'):
            print (but)
        #r2 = requests.get('http://site.ru/'+div.get('href'))
        #data2 = r2.text
        #soup2 = BeautifulSoup(data2, 'html.parser')
        ##if div.get('href').find('?user=')>0:
        ##    #print('>http://site.ru' + link.get('href'))
        ##    for link2 in soup2.find_all('a'):
        ##        link_Interno = 'http://site.ru' + link2.get('href')
        ##        if link_Interno.find('.html?') >0:
        ##            print(link_Interno)
    except OSError as err:
        print("erro")
        #print("OS error: {0}".format(err))
'''



#for link in soup.find_all('a'):
#    print(link.get('href'))


#https://gist.github.com/kennethreitz/973705
#import urllib2

#gh_url = 'https://github.com'

#auth_handler = urllib2.HTTPBasicAuthHandler()
#auth_handler.add_password(None, gh_url, 'user', 'passwd')

#opener = urllib2.build_opener(auth_handler)
#urllib2.install_opener(opener)
#handler = urllib2.urlopen(gh_url)

#print handler.getcode()
#print handler.headers.getheader('content-type')
