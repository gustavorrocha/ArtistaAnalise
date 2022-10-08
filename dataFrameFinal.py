import pandas as pd

ARTISTA = "Adele"

#df com os dados das musicas e respectivas letras 
df = pd.read_csv(f"{ARTISTA}.csv", sep=";", encoding="utf-8-sig", index_col = 0)
#tabelas de premios das musicas e dos albuns 
premios_musicas = pd.read_csv("MusicaEPremios.csv", sep=",", encoding="utf-8-sig", index_col = 0)
premios_albuns = pd.read_csv("AlbunsEPremios.csv", sep=",", encoding="utf-8-sig", index_col = 0)


def juntar_dataframes(df ,premios_musicas, premios_albuns, albuns):
    dados = df.copy()
    dados["album"] = dados.index #deixa album como uma coluna ao inves de index
    dados.reset_index(drop=True, inplace = True) #rearruma o index
    dados = dados[dados['album'].isin(albuns)] #filtra apenas os albuns de interesse
    dados['nome'] = dados['nome'].str.lower() #padroniza as strings colocando tudo em minusculo
    premios_albuns['album'] = premios_albuns['album'].apply(str) #transforma em string todos albuns
    dados = pd.merge(dados, premios_musicas, how ='left', on='nome') #agrega na base o df de premios das musicas
    dados = pd.merge(dados, premios_albuns, how ='left',  on='album') #agrega na base o df de premios dos albuns
    return dados


#junta todas as informações 
albuns = ["19", "21", "25", "30"]
dados = juntar_dataframes(df,premios_musicas, premios_albuns, albuns)


#salvando arquivo no formato csv
dados.to_csv('Adele_Com_Premios.csv', encoding="utf-8")
