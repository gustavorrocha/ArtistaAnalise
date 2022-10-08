import pandas as pd

# Cálculo do máximo e mínimo de aspectos por álbum
def max_e_min_album(df, coluna): 
    for album in df.index.get_level_values("album"): 
        info_album = df.loc[[album]]
        max_album = (info_album[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
        min_album = (info_album[["nome", coluna]].sort_values(by=[coluna])[:3])
        return pd.concat([min_album, max_album], ignore_index=True, axis=0)

# Cálculo do máximo e mínimo da aspectos em toda a discografia do artista
def max_e_min_musicas(df, coluna):
    max_musicas = (df[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
    min_musicas = (df[["nome", coluna]].sort_values(by=[coluna])[:3])
    return pd.concat([max_musicas, min_musicas], ignore_index=True, axis=0)
    
# Importa os dados do csv
ARTISTA = "Adele"
dados_df = pd.read_csv(f"./Infos/{ARTISTA}.csv", sep=";", encoding="utf-8-sig")

# Chama a função com os apectos de popularidade e duração por álbum
max_e_min_album(dados_df, "popularidade")
max_e_min_album(dados_df, "duracao")

# Chama a função com os apectos de popularidade e duração em toda a discografia do artista
max_e_min_musicas(dados_df, "popularidade")
max_e_min_musicas(dados_df, "duracao")
