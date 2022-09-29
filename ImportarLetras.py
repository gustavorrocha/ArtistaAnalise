# Importando as bibliotecas que serão utilizadas no decorrer do código
import lyricsgenius as lg


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


# Cria um objeto da classe 'Genius' que será utilizado para realizar os comandos da api, utilizando um token de autenticação
token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU" 
genius = lg.Genius(token, timeout=60, retries=10)

ARTISTA = "Adele" # Nome do artista cujos albúms serão obtidos
albums = importar_albums(ARTISTA) # Chama a função que importa os álbums
print(albums) # Imprime o que foi obtido
