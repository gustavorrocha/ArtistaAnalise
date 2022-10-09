# Importando as bibliotecas que serão utilizadas no decorrer do código
import lyricsgenius as lg
import pandas as pd
import sys


def importar_albums(nome_artista):
    """Importa os álbums de determinado artista

    :param nome_artista: Nome do artista desejado
    :type nome_artista: str
    :return: Todos os álbums desse artista
    :rtype: list[str]
    """
    
    if not isinstance(nome_artista, str):
        # Levanta um erro caso o tipo de 'nome_artista' seja inválido
        raise TypeError("O nome do artista deve ser do tipo 'str'!")

    try:
        # Obtém o objeto da classe "Artist" do artista desejado
        artist = genius.search_artist(artist_name=nome_artista, max_songs=0, get_full_info=False)
    except:
        # Caso, o artista não seja encontrado retorna um erro
        print("Ops :( Ocorreu um erro na procura do artista")
        sys.exit(2)

    # Loop para passar por todas as 'páginas' de álbums do artista
    pagina = 1
    albums_lista = []
    while pagina != None:
        albums = genius.artist_albums(artist.id, page=pagina) # Obtém os álbums do artista, com base no seu id
        pagina = albums.get("next_page") # "Descobre" se existe mais páginas de álbums

        for album in albums.get("albums"): # Para cada álbum adquiri o seu nome e id 
            nome = album.get("name") # Obtém o nome do álbum
            album_id = album.get("id") # Obtém o ID do álbum
            albums_lista.append({"id": album_id, "nome": nome}) # Insere os dados em um dicionário

    return albums_lista # Retorna a lista encontrada


def importar_letras(nome_artista):
    """Importa as letras das músicas de uma lista de álbums

    :param nome_artista: Nome do artista desejado
    :type nome_artista: str
    :return: Músicas do artista e suas respectivas letras
    :rtype: list[dict]
    """

    # Chama a função que importa os álbums
    albums = importar_albums(nome_artista) 
    
    # Loop que percorre por todos os álbums 
    musicas_dados = []
    for album in albums:

        # Obtém as músicas de cada álbum
        musicas_album = genius.album_tracks(album.get("id")) 

        # Loop que percorre por todas as músicas de um álbum
        for nome_musica in musicas_album.get("tracks"):
            num_track = nome_musica.get("number") # Obtém o número da música no álbum
            musica = nome_musica.get("song") # Utiliza o nome da música para obter dados sobre ela
            nome = musica.get("title") # Obtém o nome da música
            musica_id = musica.get("id") # Otém o ID da música
            data = musica.get("release_date_components") # Obtém a data de lançamento da música
            data = lg.utils.convert_to_datetime(data) # Converte a data para o tipo 'datetime'

            # Utiliza o id da música para obter mais informações sobre ela
            musica_dict = genius.search_song(song_id = musica_id, get_full_info=False)
            
            try:
                letra = musica_dict.lyrics # Tenta obter a letra da música
            except AttributeError: 
                letra = "" #  Caso a música não possua letra(instrumental) não interrompe o código

            # Insere os dados encontrados em uma lista
            musicas_dados.append({"album": album["nome"], "album_id": album.get("id"), "num_album": num_track, "nome": nome, "letra": letra, "musicas_album": len(musicas_album.get("tracks")),
                                  "musicas_album": len(musicas_album.get("tracks")), "data": data}) 

    return musicas_dados # Retorna a lista com os dados das músicas


def criar_df_letras(nome_artista):
    """Cria um DataFrame com as letras das músicas

    :param nome_artista: Nome do artista desejado
    :type nome_artista: str
    :return: Dataframe com as letras de todas as músicas de um artista
    :rtype: pandas.DataFrame
    """

    # Chama a função que obtém as letras das músicas
    letras_dict = importar_letras(nome_artista)

    # Obtém as chaves do dicionário que serão as colunas do DataFrame
    colunas = list(letras_dict[0].keys()) 

    # Cria uma lista com apenas os valores do dicionário com as letras
    lista_letras = []
    for musica in letras_dict:
        lista_letras.append(list(musica.values()))

    # Cria o DataFrame propriamente dito
    df_musicas = pd.DataFrame(data=lista_letras, columns=colunas) 

    return df_musicas # Retorna o DataFrame obtido


# Cria um objeto da classe 'Genius' que será utilizado para realizar os comandos da api, utilizando um token de autenticação
token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU" 
genius = lg.Genius(token, timeout=60, retries=10, remove_section_headers=True)

