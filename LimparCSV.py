# Importa as bibliotecas que serão utilizadas
import pandas as pd
import re


# Função que recebe uma lista com o caminho dos arquivos e retorna uma lista de dataframes 'limpos'
def limpar_dataframes(lista_caminhos, ignorar_variacoes = True):
    """Função que recebe uma lista com o caminho dos arquivos e retorna uma lista de dataframes 'limpos'

    :param lista_caminhos: Lista com os caminhos dos arquivos .csv
    :type lista_caminhos: list[str]
    :param ignorar_variacoes: Caso o usuário deseje manter os albúms que possuem variações deve setar como False, o padrão é True
    :type ignorar_variacoes: bool, opcional
    :return: Lista de dataframes limpos para uso
    :rtype: pandas.DataFrame
    """
    # Cria uma lista que irá armazenar os dataframes de cada caminho inserido
    lista_resultado = []

    # Loop que percorre cada caminho fornecido na função
    for caminho in lista_caminhos:
        
        # Lê o arquivo no caminho fornecido e armazena seus dados em um DataFrame
        df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", index_col=["album", "album_id", "musicas_album", 0])
        albums_unicos = set(df.index.get_level_values("album")) # Obtém todos os nomes únicos para os álbums

        # Cria uma lista para armazenar um df para cada álbum
        lista_albums = []
        for album in albums_unicos:
            # Verifica se o álbum é uma variação, caso 'ignorar_variacoes' não for definido como 'False'
            if eh_variacao(album) and ignorar_variacoes: 
                continue
            album_musicas = df.loc[[album]] # Seleciona a parte do df de cada álbum
            album_max_musicas = eliminiar_duplicata_df(album_musicas) # Obtém apenas o álbum que possui mais músicas, se tiver mais de um com mesmo nome
            album_formatado = formatar_df_album(album_max_musicas) # Aplica uma formatação no df do álbum
            lista_albums.append(album_formatado) # Adiciona o que foi obtido na lista criada
        lista_resultado.append(pd.concat(lista_albums)) # Adiciona a união do df de cada álbum na lista de resultado 

    return lista_resultado # Retorna a lista obtida


# Função que retorna se o nome do álbum revela que ele é uma variação
def eh_variacao(nome):
    """Função que retorna se o nome do álbum revela que ele é uma variação

    :param nome: Nome do álbum que será analisado
    :type nome: str
    :return: Se o nome é uma variação (com os termos "live", "remix", "edition", "promo", "exclusive", "festival")
    :rtype: bool
    """
    termos_variacao = ["live", "remix", "edition", "promo", "exclusive", "festival"] # Lista de termos que indicam um álbum de variantes
    nome_alfanum = re.sub('[^A-Za-z0-9]+', '', nome).lower() # Remove os caracteres especiais do nome do álbum
    
    # Loop que percorre todos os termos de variantes
    for termo in termos_variacao:
        if termo in nome_alfanum: # Identifica se o nome possui alguns dos termos de variação
            return True # Em caso afirmativo, retorna verdadeiro
    

# Função que recebe um DataFrame com todos os 'álbuns' que possuem o mesmo nome e retorna o que tiver mais músicas
def eliminiar_duplicata_df(df):
    """Função que recebe um DataFrame com todos os 'álbuns' que possuem o mesmo nome e retorna o que tiver mais músicas

    :param df: Dataframe com um ou mais álbums com mesmo nome
    :type df: pandas.DataFrame
    :return: Dataframe com apenas o álbum que possui o maior número de músicas
    :rtype: pandas.DataFrame
    """
    nums_album = df.index.get_level_values("musicas_album") # Obtém a quantidade de músicas dos álbums com mesmo nome
    max_num_album = max(nums_album) # Encontra a quantidade máxima de músicas do álbum
    df_max_num_album = df.iloc[df.index.get_level_values("musicas_album") == max_num_album] # DataFrame com todos os álbums com a maior quantidade de músicas
    df_max_num_album = df_max_num_album.drop_duplicates(subset=["num_album"], keep='first') # Caso exista mais de um álbum com a mesma quantidade seleciona o primeiro
    return df_max_num_album # Retorna o que foi obtido


# Função que altera a formatação do dataframe de um álbum
def formatar_df_album(df_album):
    """Função que altera a formatação do dataframe de um álbum

    :param df_album: Dataframe com informações de um álbum
    :type df_album: pandas.DataFrame
    :return: Dataframe melhor formatado com as informações do álbum
    :rtype: pandas.DataFrame
    """
    df_album.reset_index(inplace=True) # Remove o Multi-Index do data-frame
    df_album.drop(columns=["album_id", "musicas_album", "level_3"], inplace=True) # Remove as colunas que não serão mais úteis
    df_album.dropna(subset = ["num_album"], inplace=True) # Remove as colunas que não possuem valores na coluna "num_album"
    df_album["num_album"] = df_album["num_album"].apply(lambda x: int(x)) # Converte os valores da coluna "num_album" para int
    album_formatado = df_album.apply(lambda x: x.astype(str).str.strip()) # Remove espaços no início e no final de todos os elementos do df
    return album_formatado # Retorna o df após a formatação


# Função que irá juntar os dataframes dos caminhos inseridos
def juntar_dataframes(caminho_letra, caminho_dados):
    """Função que irá juntar os dataframes dos caminhos inseridos

    :param caminho_letra: Caminho do arquivo .csv com as letras das músicas
    :type caminho_letra: str
    :param caminho_dados: Caminho do arquivo .csv com os outros dados das músicas
    :type caminho_dados: str
    :return: Dataframe composto pela junção das informações dos dois CSVs
    :rtype: pandas.DataFrame
    """
    letras_df, dados_df = limpar_dataframes([caminho_letra, caminho_dados]) # Chama a função que limpa os dataframes
    letras_df_limpo = letras_df.drop(columns=["nome", "data"]) # Elimina as colunas do dataframe das letras que não serão úteis
    df = dados_df.merge(letras_df_limpo, how="inner", on=["album", "num_album"]) # Faz a junção dos dois data frames
    df.set_index(["album", "num_album"], inplace=True) # Altera o índice do dataframe final
    return df # Retorna o que foi obtido


ARTISTA = "Adele"
df = juntar_dataframes(f"./Infos/Letras - {ARTISTA}.csv", f"./Infos/Dados - {ARTISTA}.csv")
df.to_csv(f"./Infos/{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Exporta o df em um csv
