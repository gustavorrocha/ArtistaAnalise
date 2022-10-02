import pandas as pd

# Importa os dados do csv
ARTISTA = "Adele"
dados_df = pd.read_csv(f"./Infos/Dados - {ARTISTA}.csv", sep=";", encoding="utf-8-sig", index_col=["album", "album_id", "musicas_album", 0])

# Cálculo do máximo e mínimo de aspectos por álbum
def max_e_min_album(df, coluna): 
    for album in df.index.get_level_values("album"): 
        info_album = df.loc[[album]]
        print(info_album[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
        print(info_album[["nome", coluna]].sort_values(by=[coluna])[:3])

# Cálculo do máximo e mínimo da aspectos em toda a discografia do artista
def max_e_min_musicas(df, coluna):
    print(df[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
    print(df[["nome", coluna]].sort_values(by=[coluna])[:3])

# Chama a função com os apectos de popularidade e duração por álbum
max_e_min_album(dados_df, "popularidade")
max_e_min_album(dados_df, "duracao_ms")

# Chama a função com os apectos de popularidade e duração em toda a discografia do artista
max_e_min_musicas(dados_df, "popularidade")
max_e_min_musicas(dados_df, "duracao_ms")
