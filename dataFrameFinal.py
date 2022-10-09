import pandas as pd

ARTISTA = "Adele"

#df com os dados das musicas e respectivas letras 
df = pd.read_csv(f"{ARTISTA}.csv", sep=";", encoding="utf-8-sig", index_col = 0)
#tabelas de premios das musicas e dos albuns 
premios_musicas = pd.read_csv("MusicaEPremios.csv", sep=",", encoding="utf-8-sig", index_col = 0)
premios_albuns = pd.read_csv("AlbunsEPremios.csv", sep=",", encoding="utf-8-sig", index_col = 0)




def juntar_dataframes(df ,premios_musicas, premios_albuns, albuns):
    """Funçao para juntar o df com as informações das musicas e os dois dfs de premios da wikipedia
    
    :param df: DataFrame com as informações do artista, albuns, musica, letras etc
    :type df: pandas.DataFrame
    :param premios_musicas: DataFrame com as musicas premiadas e lista de premios
    :type premios_musicas: pandas.DataFrame
    :param premios_albuns: DataFrame com os albuns premiados e lista de premios
    :type premios_albuns: pandas.DataFrame
    :param albuns: lista com os albuns do cantor
    :type albuns: list[str] 
    :return: DataFrame completo com todas as informações do artista 
    :rtype: pandas.DataFrame
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(premios_musicas, pd.core.frame.DataFrame):
        raise TypeError("O premios_musicas deve ser um pd.DataFrame")
    if not isinstance(premios_albuns, pd.core.frame.DataFrame):
        raise TypeError("O premios_albuns deve ser um pd.DataFrame")
    if not isinstance(albuns, list):
        raise TypeError('A entrada albuns deve ser do tipo lista!')
    try:
        dados = df.copy()
        dados["album"] = dados.index #deixa album como uma coluna ao inves de index
        dados.reset_index(drop=True, inplace = True) #rearruma o index
        dados = dados[dados['album'].isin(albuns)] #filtra apenas os albuns de interesse
        dados['nome'] = dados['nome'].str.lower() #padroniza as strings colocando tudo em minusculo
        premios_albuns['album'] = premios_albuns['album'].apply(str) #transforma em string todos albuns
        dados = pd.merge(dados, premios_musicas, how ='left', on='nome') #agrega na base o df de premios das musicas
        dados = pd.merge(dados, premios_albuns, how ='left',  on='album') #agrega na base o df de premios dos albuns
        return dados
    except KeyError as error:
        print("Coluna inexiste: ", error)

#junta todas as informações 
albuns = ["19", "21", "25", "30"]
dados = juntar_dataframes(df,premios_musicas, premios_albuns, albuns)


#salvando arquivo no formato csv
dados.to_csv('Adele_Com_Premios.csv', encoding="utf-8")
