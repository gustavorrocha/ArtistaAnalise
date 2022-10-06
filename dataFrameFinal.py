import pandas as pd

ARTISTA = "Adele"

#df com os dados das musicas e respectivas letras 
dados = pd.read_csv(f"C:/Users/Pc/Downloads/{ARTISTA}.csv", sep=";", encoding="utf-8-sig", index_col = 0)

#Incluindo o album ocmo uma coluna do DF
dados["album"] = dados.index
dados.reset_index(drop=True, inplace = True)

#albuns de interesse
albuns = ["19", "21", "25", "30"]
dados = dados[dados['album'].isin(albuns)]
dados['nome'] = dados['nome'].str.lower() #formatando no mesmo layout dos dados das tabelas de premios


#tabelas de premios das musicas e dos albuns 
premios_musicas = pd.read_csv("MusiscaEPremios.csv", sep=",", encoding="utf-8-sig", index_col = 0)
premios_albuns = pd.read_csv("AlbunsEPremios.csv", sep=",", encoding="utf-8-sig", index_col = 0)

#mudança do tipo de dado da coluna album para string
premios_albuns.rename(columns = {'nome': 'album'}, inplace = True)
premios_albuns['album'] = premios_albuns['album'].apply(str)

#juntando os 3 dfs 
dados = pd.merge(dados, premios_musicas, how ='left', on='nome')
dados = pd.merge(dados, premios_albuns, how ='left',  on='album')


#salvando arquivo no formato csv
dados.to_csv('Adele_Com_Premios.csv', encoding="utf-8")
