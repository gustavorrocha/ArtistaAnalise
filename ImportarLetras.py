# Importando as bibliotecas que serão utilizadas no decorrer do código
import lyricsgenius as lg
import pandas as pd


# Função que importa os álbums de determinado artista
def importar_albums(nome_artista):

    # Obtém o objeto da classe "Artist" do artista desejado
    artist = genius.search_artist(nome_artista, max_songs=0, get_full_info=False) 

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


# Função que importa as letras das músicas de uma lista de álbums
def importar_letras(nome_artista):

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
            musicas_dados.append({"album": album["nome"], "num_album": num_track, "nome": nome, "letra": letra, "data": data}) 

    return musicas_dados # Retorna a lista com os dados das músicas


# Função que cria um DataFrame com as letras das músicas
def criar_df_letras(nome_artista):

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
genius = lg.Genius(token, timeout=60, retries=10)

ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
df_letras = criar_df_letras(ARTISTA) # Cria um DataFrame com as letras do artista escolhido
df_letras.to_csv(f"./Letras/{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Exporta o df em um csv
