# Importando as bibliotecas que serão utilizadas no decorrer do código
import spotipy
import pandas as pd


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
                albums_lista.append({"id" : album_id, "nome" : album_name, 
                "data" : album_release_date, "num_musicas" : album_num_tracks})

    return albums_lista # Retorna a lista de álbums obtida


# Função que ira obter os dados de cada música
def obter_dados(nome_artista, tipos_album):

    # Utiliza a função criada para obter os álbums do artista
    albums = encontrar_albums(nome_artista, tipos_album) 

    # Loop que percorre por todos os álbums 
    musicas_dados = []
    for album in albums:

        # Obtém as músicas de cada álbum
        musicas_album = sp.album_tracks(album.get("id")).get("items")

        # Cria uma lista com os IDs das músicas do álbum (uma vez que alguns dados só são obtidos dessa forma)
        musicas_album_ids = list(map(lambda msc: msc.get("id"), musicas_album))

        # Função que recebe uma lista de IDs e retorna dados sobre as músicas
        musicas = sp.tracks(musicas_album_ids)

        # Loop que percorre por todas as músicas de um álbum
        for musica in musicas.get("tracks"):
            num_track = musica.get("track_number") # Obtém o número da música no álbum
            musica_id = musica.get("id") # Otém o ID da música
            musica_nome = musica.get("name") # Obtém o nome da música
            musica_popularidade = musica.get("popularity") # Obtém a popularidade da música
            musica_explicita = musica.get("explicit") # "Decobre" se a música possui letra explícita
            musica_duracao_ms = musica.get("duration_ms") # Obtém a duração da música (em ms)

            # Obtém uma string com todos os artistas da música separados por '/'
            musica_artistas_lista = list(map(lambda art: art.get("name"), musica.get("artists")))
            musica_nomes_artistas = "/".join(musica_artistas_lista)

            # Obtém algumas 'features' de cada música
            musica_features = sp.audio_features(musica_id)[0]
            musica_volume = musica_features.get("loudness") # Armazena o volume da música
            musica_bpm = musica_features.get("tempo") # Armazena o bpm da música
            musica_dancabilidade = musica_features.get("danceability") # Armazena a dançabilidade da música
            musica_energia = musica_features.get("energy") # Armazena a energia da música
            musica_fala = musica_features.get("speechiness") # Armazena o nível de fala da música
            musica_acustica = musica_features.get("acousticness") # Armazena o nível de acústica da música
            musica_instrumentalidade = musica_features.get("instrumentalness") # Armazena o nível de instumentalidade da música
            musica_vivacidade = musica_features.get("liveness") # Armazena a vivacidade da música
            musica_valencia = musica_features.get("valence") # Armazena a valência da música

            # Informações musicais que podem não ser utilizadas
            musica_chave = musica_features.get("key") # Armazena a chave da música
            musica_modo = musica_features.get("mode") # Armazena o modo da música
            musica_assinatura_tempo = musica_features.get("time_signature") # Armazena a assinatura do tempo da música

            # Insere os dados encontrados em uma lista de dicionarios
            musicas_dados.append({"album": album["nome"], "num_album": num_track, "nome": musica_nome, "data": album["data"], 
            "artistas": musica_nomes_artistas, "popularidade": musica_popularidade, "letra_explicita": musica_explicita, 
            "duracao_ms": musica_duracao_ms, "volume": musica_volume, "bpm": musica_bpm, "energia": musica_energia, 
            "dancabilidade": musica_dancabilidade, "vivacidade": musica_vivacidade, "fala": musica_fala, 
            "acustica": musica_acustica, "instrumentalidade": musica_instrumentalidade, "valencia": musica_valencia, 
            "chave": musica_chave, "modo": musica_modo, "assinatura_tempo": musica_assinatura_tempo}) 

    return musicas_dados # Retorna a lista com os dados das músicas


# Função que cria um DataFrame com os dados das músicas
def criar_df_dados(nome_artista, tipos_album):

    # Chama a função que obtém os dados das músicas
    dados_dict = obter_dados(nome_artista, tipos_album)

    # Obtém as chaves do dicionário que serão as colunas do DataFrame
    colunas = list(dados_dict[0].keys()) 

    # Cria uma lista com apenas os valores do dicionário com os dados
    lista_dados = []
    for musica in dados_dict:
        lista_dados.append(list(musica.values()))

    # Cria o DataFrame propriamente dito
    df_musicas = pd.DataFrame(data=lista_dados, columns=colunas) 

    return df_musicas # Retorna o DataFrame obtido


# Dados que serão utilizados para autenticação
id = "aec45161707e49dea708fb56dfa88983"
secret = "688ff38871c343b99b08c034787aea7c"

# Cria um objeto da classe 'Spotify' que será utilizado para realizar os comandos da api, utilizando dois dados de autenticação
credenciais = spotipy.oauth2.SpotifyClientCredentials(client_id=id, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=credenciais)
    
ARTISTA = "Adele" # Nome do artista cujos dados musicais serão obtidas
df_dados = criar_df_dados(ARTISTA, ["album", "single"]) # Cria um DataFrame com os dados das músicas do artista escolhido
df_dados.to_csv(f"./Dados/{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Exporta o df em um csv
