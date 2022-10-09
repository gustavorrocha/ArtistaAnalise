import pandas as pd
import numpy as np
import scipy
import seaborn as sns

import AnaliseArtista as AA


# Importa os dados do csv
ARTISTA = "Adele"
df = pd.read_csv(f"C:/Users/Pc/Downloads/{ARTISTA}_Com_Premios.csv", sep=",", encoding="utf-8-sig", index_col = 0)
df.set_index('album',inplace = True)

#==================================================================================  
#GRUPO DE PERGUNTAS 1

# i Músicas mais ouvidas e músicas menos ouvidas por Álbum
AA.max_e_min_album(df, "popularidade")

# ii Músicas mais longas e músicas mais curtas por Álbum
AA.max_e_min_album(df, "duracao")


# iii Músicas mais ouvidas e músicas menos ouvidas [em toda a história da banda ou artista]
AA.max_e_min_musicas(df, "popularidade")

# iv Músicas mais longas e músicas mais curtas [em toda a história da banda ou artista]
AA.max_e_min_musicas(df, "duracao")

# v albuns mais premiado
AA.albuns_mais_premiados(df, 3)

# vi Existe alguma relação entre a duração da música e sua popularidade?
AA.corr_com_tempo(df, "popularidade") 


 

#GRUPO DE PERGUNTAS 1 - VISUALIZAÇÃO 

# Visualização do máximo e mínimo de aspectos por álbum
AA.visualizacao_maxmin_album(df, "popularidade")

# Visualização do máximo e mínimo de aspectos em toda a discografia do artista
AA.visualizacao_maxmin_musicas(df, "popularidade")



#==================================================================================   
#GRUPO DE PERGUNTAS 3

# Comparar duas colunas do data frame por meio de visualização grafica e de regressão linear
AA.plot(df, 'vivacidade' ,'popularidade')
AA.plot(df, 'dancabilidade' ,'energia')

# Comparar popularidade media do album com quantidade de premiações do album e suas musica
AA.comparar_popularidade_premios(df)

#  Frenquencia do modo (maior ou menor) de toda a discografia, por album ou por musica.
AA.porcentagem_modo(df, "album")
AA.porcentagem_modo(df, "musica")