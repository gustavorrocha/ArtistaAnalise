import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cálculo do máximo e mínimo de aspectos por álbum
def max_e_min_album(df, coluna): 
    for album in set(df.index.get_level_values("album")): 
        info_album = df.loc[[album]]
        max_album = (info_album[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
        min_album = (info_album[["nome", coluna]].sort_values(by=[coluna])[:3])
        return pd.concat([min_album, max_album], ignore_index=True, axis=0)

# Cálculo do máximo e mínimo da aspectos em toda a discografia do artista
def max_e_min_musicas(df, coluna):
    max_musicas = (df[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
    min_musicas = (df[["nome", coluna]].sort_values(by=[coluna])[:3])
    return pd.concat([max_musicas, min_musicas], ignore_index=True, axis=0)

# Visualização do máximo e mínimo de aspectos em toda a discografia do artista
def visualizacao_maxmin_musicas(df, coluna):
    principal = max_e_min_musicas(df, coluna)
    fig = sns.barplot(data = principal, x = "nome", y = coluna)
    return plt.show ()
   
# Álbuns mais premiados
def albuns_mais_premiados(df, top):
    dfcopy = df.copy()
    dfcopy = dfcopy[dfcopy["premios do album"].notnull()][["premios do album"]].drop_duplicates()
    dfcopy["quantidade de premios"] = dfcopy["premios do album"].str.split(" & ").apply(len)
    return dfcopy[:top][["quantidade de premios"]]

# Existe alguma relação entre a duração da música e sua popularidade?
def corr_com_tempo(df, variavel):
    dfcopy = df.copy()
    minutos = dfcopy["duracao"].str.split(":", expand=True)[0].apply(int)*60
    segundos = dfcopy["duracao"].str.split(":", expand=True)[1].apply(int)
    duracao = np.array(minutos + segundos)
    var = np.array(dfcopy[variavel].apply(float))
    print(f"A correlção entre a duração da musica e {variavel} é: ")
    return np.corrcoef(duracao, var)[0][1] 
    
# Importa os dados do csv
ARTISTA = "Adele"
dados_df = pd.read_csv(f"./Infos/{ARTISTA}.csv", sep=";", encoding="utf-8-sig")

# Chama a função com os apectos de popularidade e duração por álbum
max_e_min_album(dados_df, "popularidade")
max_e_min_album(dados_df, "duracao")

# Chama a função com os apectos de popularidade e duração em toda a discografia do artista
max_e_min_musicas(dados_df, "popularidade")
max_e_min_musicas(dados_df, "duracao")

# Chama a visualização com os apectos de popularidade e duração em toda a discografia do artista
visualizacao_maxmin_musicas(dados_df, "popularidade")
visualizacao_maxmin_musicas(dados_df, "duracao")

# Chama a função com os albuns mais premiados 
albuns_mais_premiados(df, 3)  

# Chama a função com a correlação entre duração da música e alguma variável
corr_com_tempo(df,"popularidade")

