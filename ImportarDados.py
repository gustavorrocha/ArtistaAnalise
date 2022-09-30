import spotipy


# Funçao que encontra determinados tipos de álbum de um artista
def encontrar_albums(nome_artista, tipos_album):

    # Obtém dados sobre o artista através de uma pesquisa
    artista = sp.search(nome_artista, type="artist", limit=1) 

    # Armazena o ID do artista em uma variável
    id_artista = artista.get("artists").get("items")[0].get("id")

    # Checa se a lista de tipos de álbum inserida é válida e "levanta" uma exceção caso não seja
    possiveis_tipos = {"album", "single", "appears_on", "compilation"}
    if set(tipos_album).issubset(possiveis_tipos) == False: 
        raise ValueError

    # Loop para percorrer todos os todos os tipos de álbum e armazenar os dados em uma lista
    albums_lista = []
    for tipo in tipos_album:
        i = 0 # Cria uma variável acumulativa
        proximos_albums = "" # Inicia a variável que identificará se existem mais álbums
        while proximos_albums != None: # Enquanto existe mais uma página continua executando
            albums = sp.artist_albums(id_artista, limit=50, offset=i, album_type=tipo) # Obtém os álbums do artista, com base no seu id
            proximos_albums = albums.get("next") # "Descobre" se existe mais páginas de álbums
            i += 50 # Incrementa a variável acummulativa que armazena o offset

            # Adquire informações de cada álbum
            for album in albums.get("items"): 
                album_id = album.get("id") # Obtém o ID do álbum
                album_name = album.get("name") # Obtém o nome do álbum
                album_release_date = album.get("release_date") # Obtém a data de lançamento do álbum
                album_num_tracks = album.get("total_tracks") # Obtém o número de músicas do álbum
                
                # Insere os dados encontrados em um dicionário
                albums_lista.append({"id" : album_id, "name" : album_name, 
                "release_date" : album_release_date, "num_tracks" : album_num_tracks})

    return albums_lista


# Dados para autenticação
id = "aec45161707e49dea708fb56dfa88983"
secret = "688ff38871c343b99b08c034787aea7c"

# Cria um objeto da classe 'Spotify' que será utilizado para realizar os comandos da api, utilizando dois dados de autenticação
credenciais = spotipy.oauth2.SpotifyClientCredentials(client_id=id, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=credenciais)
    
ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
albums = encontrar_albums(ARTISTA, ["single", "album"]) # Utiliza a função criada para obter os álbums do artista
print(albums) # Imprime o que foi obtido
