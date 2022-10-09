Exemplo de Uso
=================

Para demonstrar a utilização do pacote foi feito um exemplo de uso utilizando uma série de perguntas, que forma respondidas com base nos dados das músicas da cantora 'Adele':

Primeiro, é necessário criar a base de dados, para isso deve-se utlizar as funções na seção 'Gerador da Base de Dados'.

Para isso é necessário chamar algumas funções, que irão criar três arquivos '.csv' na pasta chamada 'Infos', um com as letras das músicas, um com outros dados da discografia e, por último, um com os dados unidos:

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas

    df_letras = SpotifyImport.criar_df_letras(ARTISTA) # Cria um DataFrame com as letras do artista escolhido
    df_letras.to_csv(f"./Infos/Letras - {ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Exporta o df em um csv

    df_dados = SpotifyImport.criar_df_dados(ARTISTA, ["album", "single"]) # Cria um DataFrame com os dados das músicas do artista escolhido
    df_dados.to_csv(f"./Infos/Dados - {ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Exporta o df em um csv

    df = LimparCSV.juntar_dataframes(f"./Infos/Letras - {ARTISTA}.csv", f"./Infos/Dados - {ARTISTA}.csv")
    df.to_csv(f"./Infos/{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Exporta o df em um csv


Agora que temos um arquivo chamado 'Adele.csv' com as informações de todas as músicas da Adele, podemos começar a fazer as análises.

Grupo de Perguntas 1:
-----------------------

* Músicas mais ouvidas e músicas menos ouvidas por Álbum:

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado


* Músicas mais longas e músicas mais curtas por Álbum:

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado


* Músicas mais ouvidas e músicas menos ouvidas [em toda a história da banda ou artista]:

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado


* Músicas mais longas e músicas mais curtas [em toda a história da banda ou artista]:

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado


* Álbuns mais premiados:

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado


* Existe alguma relação entre a duração da música e sua popularidade?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado



Grupo de Perguntas 2:
-----------------------

Nesse grupo de perguntas, foi criado também TagClouds com as infromações obtidos nos primeiros 4 tópicos.

* Quais são as palavras mais comuns nos títulos dos Álbuns?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado

    # Imprime as palavras mais comuns e cria a tagcloud
    print(palavras_comuns(df, "nome", "./Imgs/nome.png")) 


Saída: [('30', 1), ('21', 1), ('19', 1)]
   

* Quais são as palavras mais comuns nos títulos das músicas?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado

    # Imprime as palavras mais comuns e cria a tagcloud
    print(palavras_comuns(df, "album", "./Imgs/album.png")) 


Saída: [('love', 6), ('heart', 2), ('like', 2)]


* Quais são as palavras mais comuns nas letras das músicas, por Álbum?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado

    # Imprime um dicionário com as palavras mais comuns e cria as tagclouds
    print(gerar_tag_cloud_por(df, "letra", "./Imgs/Albums", "album")) 


    Saída: {25: [('like', 32), ('go', 27), ("i'm", 26)], 19: [("i'm", 44), ('love', 26), ('aye', 24)], 21: [('love', 44), ("i'll", 27), ('take', 23)], 30: [("i'm", 37), ('love', 27), ('get', 27)]}


* Quais são as palavras mais comuns nas letras das músicas, em toda a discografia?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado

    # Imprime as palavras mais comuns e cria a tagcloud
    print(palavras_comuns(df, "letra", "./Imgs/letra.png")) 


Saída: [("i'm", 127), ('love', 117), ('like', 94)]


* O título de um álbum é tema recorrente nas letras?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado

    # Imprime um dicionário com a proporção entre as palavras no álbum e nas letras de suas músicas
    print(proporção_comparativa(df, "letra", "album")) 


Saída: {25: '0/2725', 19: '0/2884', 21: '0/2810', 30: '0/2898'}


* O título de uma música é tema recorrente nas letras?

.. code-block:: python

    ARTISTA = "Adele" # Nome do artista cujas letras serão obtidas
    df = pd.read_csv(f"./{ARTISTA}.csv", sep=";", encoding="utf-8-sig") # Lê o arquivo criado

    # Imprime um dicionário com a proporção entre as palavras no título da música e a sua letra
    print(proporção_comparativa(df, "letra", "nome"))


Saída: {'Love In The Dark': '15/235', 'Strangers By Nature': '5/133', 'Daydreamer': '2/194', 'All Night Parking Interlude': '12/169', 'One And Only': '11/195', 'Can I Get It': '72/270', 'Hold On': '29/199', "He Won't Go": '11/222', 'I Found A Boy': '31/252', 'I Drink Wine': '22/325', 'Turning Tables': '18/253', 'Water Under the Bridge': '33/252', 'When We Were Young': '21/227', 'All I Ask': '17/207', "Don't You Remember": '32/198', 'Rolling in the Deep': '49/344', 'Love Is A Game': '23/261', 'My Same': '4/334', 'My Little Love': '10/202', 'Lovesong': '0/186', 'Hometown Glory': '4/245', 'Oh My God': '11/274', 'Remedy': '5/265', 'Easy On Me': '21/207', 'Best For Last': '10/312', 'Crazy For You': '26/184', 'Rumour Has It': '39/211', 'To Be Loved': '20/258', 'Take It All': '57/265', 'Cold Shoulder': '8/293', 'Make You Feel My Love': '36/187', 'Million Years Ago': '9/289', "I'll Be Waiting": '30/274', 'River Lea': '40/361', 'Sweetest Devotion': '8/223', 'Cry Your Heart Out': '37/261', 'Someone Like You': '17/235', 'Chasing Pavements': '18/290', 'Right As Rain': '12/234', 'Woman Like Me': '17/339', 'Melt My Heart To Stone': '27/242', 'Send My Love': '8/174', 'First Love': '19/166', 'Hello': '7/256', 'I Miss You': '16/236', 'Tired': '5/203', 'Set Fire to the Rain': '14/175'}


Grupo de Perguntas 3: 
-----------------------

Elaborar mais 3 perguntas sobre temas e características da discografia da banda.