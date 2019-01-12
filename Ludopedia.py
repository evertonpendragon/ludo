import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def getGameInfo(pagina):
    # abre a pagina
    page = requests.get(pagina)

    # se a página foi baixada com sucesso = 200
   # print("status_code: ",page.status_code)

    # elementos da página
    # list(soup.children)


    # exibe conteúdo da página
    # page.content

    # texto da pag
    data = page.text

    soup = BeautifulSoup(data, 'html.parser')

    # encontra os links
    # for link in soup.find_all('a'):
    # print(link.get('href'))


    #titulo
    titulo = soup.find('div', class_="jogo-top-main")
    titulo =  titulo.find('a', href="#").text.strip()
    #print(titulo)

    #ano
    ano = soup.find('div', class_="jogo-top-main")
    ano =  ano.find('span', class_=" text-xs").text.strip()
    print(titulo, ano)


    #Rank
    #for div in soup.find_all('div', class_="jogo-top-capa"):
    rank=[]
    item =  soup.find('div', class_="mar-top hidden-xs")
    for x in item.find_all(class_="block"):
        #print(x.contents)
        #isso tbm funciona, mas é mais trabalhodo->#print(x.contents[0],x.contents[1].find('a').contents[0]) ## ['Rank: ', <span><u><a class="text-bold" href="https://www.ludopedia.com.br/search_jogo">25</a></u></span>]
        rank.append( {x.contents[0].replace(': ',''):x.contents[1].text.strip()} )## ['Rank: ', <span><u><a class="text-bold" href="https://www.ludopedia.com.br/search_jogo">25</a></u></span>]
    #print(rank)
    #Tenho, quero, tive, favorito
    listaDesejos=[]
    for div in soup.find_all(class_="btn-colecao"):
        for item in  list(div):
            colecao, qtd = (item.split())
            qtd= ''.join( [numero for numero in qtd if numero.isdigit()  ])
            listaDesejos.append( {colecao:qtd})
    #print(listaDesejos)


    #mercado
    anuncios = []
    blkAnuncio = soup.find(id="bloco-anuncios-sm")

    linkAnuncio = blkAnuncio.find('div', class_="btn-group")
    linkAnuncio = (linkAnuncio.find('a')['href'])

    pgAnuncio = requests.get(linkAnuncio)
    pgAnuncio = BeautifulSoup(pgAnuncio.text, 'html.parser')

    blkAnuncio = pgAnuncio.find('div', id="anuncios")
    #print(blkAnuncio)
    if blkAnuncio != None:
        for table in blkAnuncio.findAll('table'):
            rows = table.find_all('tr')
            for row in rows:
                #print("row: " , type(row))
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                anuncios.append([ele for ele in cols ])  # Get rid of empty values
        qtdAnuncios= {"Anuncios": len(anuncios)-1}
    else:
        qtdAnuncios={"Anúncios":0}
    #print(qtdAnuncios)
    #print(anuncios)
    registro = [titulo,ano,rank,listaDesejos,qtdAnuncios,anuncios]
    print(
        "______________________________________________________________________________________________________________________")
    return (registro)



#########################################################################################################################



for i in range(1,201):
    print("Página",i)

    paginaPrincipal="https://www.ludopedia.com.br/search_jogo?pagina="+str(i)
    page = requests.get(paginaPrincipal)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')

    listaJogos = soup.find('div', id="resultado anchor")
    for jogo in listaJogos.find_all('div',class_="media-body"):
        link = jogo.find('a')['href']
        linha = str(getGameInfo(link))+"\n"

        arq = open('C:/Users/Everton/Desktop/ludopedia.txt', 'a',encoding="utf-8")
        arq.write((linha))
        arq.close()
