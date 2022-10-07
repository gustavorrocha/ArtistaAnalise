import pandas as pd
import requests
from bs4 import BeautifulSoup

#web Scraping das tabelas de premios da Adela da Wikipedia


wikiurl="https://pt.wikipedia.org/wiki/Lista_de_prêmios_e_indicações_recebidos_por_Adele"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
#200 -> sucesso no request

soup = BeautifulSoup(response.text, 'html.parser')
tables =soup.find_all('table',{'class':"wikitable"})



#-----------------------------------------------
#montagem do DataFrame com todas tabelas da Wiki
dfs = []
k = 1
for i in tables:
    try:
        df = pd.read_html(str(i))[0].dropna(how="all", axis=1).dropna() 
        instituicao = df.columns.get_level_values(0)[0]
        df.columns = df.columns.get_level_values(1).str.lower()
        df["instituicao"] = instituicao
        df["numero"] = k
        try:
            df.ano = df.ano.str.split("[",expand = True)[0]
        except AttributeError:
            pass
        k+=1
        dfs.append(df)
    except IndexError:
        #Existe uma tabela com formatação diferente que sera tratada excepcionalmente
        df = pd.read_html(str(i))[0].dropna(how="all", axis=1).dropna()
        #como a tabela tem formatção diferente, normalizo os nomes das colunas 
        df.rename(columns={'Prêmio': 'trabalho nomeado', 'Situação': 'resultado' }, inplace = True)
        df.columns = df.columns.get_level_values(0).str.lower()
        instituicao = "Kids' Choice Awards"
        df["instituicao"] = instituicao
        dfs.append(df)
        

#reinicia o indice
df = pd.concat(dfs).reset_index(drop=True)

#tiranod " dos nomes
df["trabalho nomeado"] = df["trabalho nomeado"].astype(str).apply(lambda x: x.replace('"',""))

#tiarando hiperlinks da wikipedia
df["resultado"] = df["resultado"].str.split("[", expand=True)[0]

#desconsiderando a coluna de REF
df = df[df.columns[:-1]]

#premio = 'instituição + ano + categoria do premio
df["premio"] = (df["instituicao"]
                .add(" ")
                .add(df["ano"].astype(str))
                .add(": ")
                .add(df["categoria"])
               )

#transforma tudo em string
df = df.astype(str)


#mudanças realizadas na coluna trabalho para normalizar os dados 
changes = {"adele at the bbc" : "adele",
          "need you now com" : "need you now",
          "adele: one night only" : "one night only",
          "artista favorito ur" : "adele",
            '“send my love': 'send my love'}

#aplicando mudanças 
df["trabalho nomeado"] = (df["trabalho nomeado"]
                         .str.split("(", expand=True)[0]
                         .str.split(".", expand=True)[0]
                         .str.lower().str.strip()
                         .replace(changes)
                         )


#Data frame contendo apenas os premios que Adele ganhou
dfp = df[df.resultado == "Venceu"][["trabalho nomeado","premio"]]
dfp = dfp[dfp["trabalho nomeado"] != "adele"].reset_index(drop=True)


#------------------------------------------
#DataFrame com ALbuns e repsectivos premios 
albuns = ["21","19", "25"]
dfp_albuns = dfp[dfp["trabalho nomeado"].isin(albuns)]


g = dfp_albuns.groupby("trabalho nomeado")

#junta todos os premios em uma lista
album_compressed = []
for data in g:
    album_compressed.append((data[0], " & ".join(list(data[1].premio.values))))

#df final com os albuns e respectiva lista de premios    
album_compressed = pd.DataFrame(album_compressed, columns = ["album", "premios do album"])



#------------------------------------------
#DataFrame com Musicas e repsectivos premios 
dfp_musicas = dfp[~dfp["trabalho nomeado"].isin(albuns)]

g = dfp_musicas.groupby("trabalho nomeado")

#junta todos os premios em uma lista
music_compressed = []
for data in g:
    music_compressed.append((data[0], " & ".join(list(data[1].premio.values))))
    
#df final com as musicas e respectiva lista de premios
music_compressed = pd.DataFrame(music_compressed, columns = ["nome", "premios da musica"])


#------------------------------------------
#salvando as tabelas em arquivos csv

music_compressed.to_csv('MusiscaEPremios.csv', encoding="utf-8")

album_compressed.to_csv('AlbunsEPremios.csv', encoding="utf-8")

