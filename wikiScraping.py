import pandas as pd
import requests
from bs4 import BeautifulSoup


#função para pegar todas as tabelas da pagina da wiki
def pegar_wikipedia_tabelas_html(wikiurl):
    try:
        if not isinstance(wikiurl, str):
            raise TypeError("A entrada deve ser uma string!")
        
        response=requests.get(wikiurl)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tables =soup.find_all('table',{'class':"wikitable"})
        return tables
    
    except requests.exceptions.HTTPError as errh:
        print ("Erro no http:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Erro na Conecção:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Erro por Tempo Esgotado:",errt)
    except requests.exceptions.RequestException as err:
        print ("Ops. Alguma outra coisa aconteceu!",err) 
        

#cria um df conjunto de todas tabelas
def juntar_tabelas_html(tabelas):
    dfs = []
    for i in tabelas:
        try:
            df = pd.read_html(str(i))[0].dropna(how="all", axis=1).dropna() 
            instituicao = df.columns.get_level_values(0)[0]
            df.columns = df.columns.get_level_values(1).str.lower()
            df["instituicao"] = instituicao
            dfs.append(df) 
        except IndexError:
            df = pd.read_html(str(i))[0].dropna(how="all", axis=1).dropna()
            df.rename(columns={'Prêmio': 'trabalho nomeado', 'Situação': 'resultado' }, inplace = True)
            df.columns = df.columns.get_level_values(0).str.lower()
            instituicao = "Nao Especificado"
            df["instituicao"] = instituicao
            dfs.append(df)
    df = pd.concat(dfs).reset_index(drop=True) #restaura o index
    df = df[df.columns[:-1]] #retira ultima coluna de ref
    df = df.astype(str)#padroniza o tipo de dados
    return df


#retira das colunas as partes entre parenteses ou depois de caracteries especificos
def limpar_coluna(df, coluna, caracteres):
    for caracter in caracteres:
        df[coluna] = df[coluna].str.split(f"{caracter}", expand=True)[0].str.lower().str.strip()   


#altera algumas strings erradas na base        
def substituir_strings(df, coluna, changes):
    df[coluna] = df[coluna].astype(str).apply(lambda x: x.replace('"',""))
    df[coluna] = df[coluna].replace(changes)


#cria uma coluna denominada premio que contempla a 'instituição que premia'
# + o 'ano' no qual o premio foi concedido e 'categoria' ganha. 
def adicionar_coluna_premio(df):
    df["premio"] = (df["instituicao"]
                .add(" ")
                .add(df["ano"].astype(str))
                .add(": ")
                .add(df["categoria"])
                )    

 
#função que cria dois dataframes discriminando o que é premio de album e musica
def df_premios(df, albuns):
    dfp = df[df["resultado"] == "venceu"][["trabalho nomeado","premio"]] #desconsidera premios nao ganhos
    dfp = dfp[dfp["trabalho nomeado"] != "adele"].reset_index(drop=True) #desconsidera premios da personalidade Adele    
    
    #cria df apenas com albuns e lista d premios:
    dfp_albuns = dfp[dfp["trabalho nomeado"].isin(albuns)] #separa df com premios dos albuns
    a = dfp_albuns.groupby("trabalho nomeado")
    album_compressed = []
    for data in a: #itera em todos os premios e cria uma lista com todos premios na coluna
        album_compressed.append((data[0], " & ".join(list(data[1].premio.values))))  
    album_compressed = pd.DataFrame(album_compressed, columns = ["album", "premios do album"]) #cria df final e renomeia colunas
    
    #cria df apenas com musicas e lista d premios;
    dfp_musicas = dfp[~dfp["trabalho nomeado"].isin(albuns)] #separa df com premios das musicas (que nao sao dos albuns)
    m = dfp_musicas.groupby("trabalho nomeado")
    music_compressed = []
    for data in m: #itera em todos os premios e cria uma lista  com todos premios na coluna
        music_compressed.append((data[0], " & ".join(list(data[1].premio.values))))
    music_compressed = pd.DataFrame(music_compressed, columns = ["nome", "premios da musica"]) #cria df final e renomeia colunas

    return album_compressed, music_compressed


    
#pegar todas tabelas de premios da wiki da Adele    
html_tabelas = pegar_wikipedia_tabelas_html("https://pt.wikipedia.org/wiki/Lista_de_pr%C3%AAmios_e_indica%C3%A7%C3%B5es_recebidos_por_Adele")


#juntar todas as tabelas em um unico df
df = juntar_tabelas_html(html_tabelas)

#limpar valores indevidos nas colunas
limpar_coluna(df, 'trabalho nomeado', ['(', '.'])
limpar_coluna(df, 'resultado', ['['])
limpar_coluna(df, 'ano', ['['])
mudancas =  {"adele at the bbc" : "adele",
            "need you now com" : "need you now",
            "adele: one night only" : "one night only",
            "artista favorito ur" : "adele",
            '“send my love': 'send my love'}
substituir_strings(df, "trabalho nomeado", mudancas)
adicionar_coluna_premio(df)


#cria tabelas distintas para premiações dos albuns e das musicas 
albuns = ["21","19", "25", "30"]
album_compressed, music_compressed = df_premios(df, albuns)

#salvando as tabelas em arquivos csv
music_compressed.to_csv('MusicaEPremios.csv', encoding="utf-8")
album_compressed.to_csv('AlbunsEPremios.csv', encoding="utf-8")

