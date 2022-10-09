# Importando as bibliotecas que serão utilizadas
import wordcloud
import pandas as pd
from collections import Counter
import re
from nltk.corpus import stopwords
import sys


def palavras_comuns(df, coluna, caminho, idioma = "english", ignorar_stopwords = True):
    """Encontra as plavras mais comuns e cria uma 'tag cloud', com os dados de uma das colunas do dataframe

    :param df: Dataframe que será utilizado para a criação dos dados
    :type df: pandas.DataFrame
    :param coluna: Título da coluna cujos dados serão obtidos
    :type coluna: str
    :param caminho: Caminho onde o arquivo png da tag cloud será gerada
    :type caminho: str
    :param idioma: Idioma das palavras do DataFrame, padrão é "english"
    :type idioma: str, optional
    :param ignorar_stopwords: Se a contagem deve ignorar stopwords, padrão é True
    :type ignorar_stopwords: bool, optional
    :return: Palavras mais comuns da coluna desejada
    :rtype: list[tuples]
    """

    if not isinstance(df, pd.DataFrame):
        # Levanta um erro caso o tipo de 'df' seja inválido
        raise TypeError("A variável 'df' deve ser um Dataframe!")
    if not isinstance(caminho, str):
        # Levanta um erro caso o tipo de 'caminho' seja inválido
        raise TypeError("A variável 'caminho' deve ser do tipo 'str'!")
    if not isinstance(ignorar_stopwords, bool):
        # Levanta um erro caso o tipo de 'ignorar_stopwords' seja inválido
        raise TypeError("A variável 'ignorar_stopwords' deve ser do tipo 'bool'!")

    try:
        # Cria uma lista com as 'stopwords'
        palavras_ignoradas = stopwords.words(idioma) 
    except OSError:
        # Caso as stopwords não sejam encontradas, interrmpoe a execução
        print(f"Idioma '{idioma}' não encontrado! A lista de idiomas válidos é: {stopwords.fileids()}")
        sys.exit()
    
    if ignorar_stopwords:
        # Cria o objeto que gera Tag Clouds com stopwords
        wc = wordcloud.WordCloud(stopwords=palavras_ignoradas, width=1720, height=1080) 
    else:
        # Cria o objeto que gera Tag Clouds sem stopwords
        wc = wordcloud.WordCloud(stopwords=[], width=1720, height=1080)

    if coluna not in df.columns:
        # Checa se existe a coluna fornecida no Dataframe
        raise ValueError(f"Não existe a coluna {coluna} no DataFrame fornecido!")

    unicos = set(df[coluna].tolist()) # Encontra os valores únicos nessa coluna
    unicos_str = {str(elemento) for elemento in unicos} # Transforma cada elemento em string
    palavras = " ".join(unicos_str) # Junta todos esses elementos em uma só string
    palavras = re.sub('[^A-Za-z0-9\']+', ' ', palavras).lower()

    try:
        # Chama a função para gerar as Tag Clouds
        wc.generate(palavras).to_file(caminho) 
    except ValueError:
        # Caso não haja palavras válidas para gerar a tag cloud imprime uma mensagem ao usuário
        print(f"Não foi possivel gerar uma tag cloud com os dados de {coluna}!")

    if ignorar_stopwords:
        return palavras_mais_comuns(palavras, 3, palavras_ignoradas)
    else:
        return palavras_mais_comuns(palavras, 3, [])
    

def palavras_mais_comuns(texto, quantidade, palavras_ignoradas):
    """Encontra as palavras mais comuns de uma string

    :param texto: Texto que se objetiva encontrar as palavras mais comuns
    :type texto: str
    :param quantidade: Número de palavras que se deseja
    :type quantidade: int
    :param palavras_ignoradas: Palavras que não serão consideradas na contagem
    :type palavras_ignoradas: list[str]
    :return: Palavras mais comuns do texto
    :rtype: list[tuples]
    """

    if not isinstance(texto, str):
        # Levanta um erro caso o tipo de 'texto' seja inválido
        raise TypeError("A variável 'texto' deve ser uma string!")
    if not isinstance(quantidade, int):
        # Levanta um erro caso o tipo de 'quantidade' seja inválido
        raise TypeError("A variável 'quantidade' deve ser um número inteiro!")
    if not isinstance(palavras_ignoradas, list):
        # Levanta um erro caso o tipo de 'palavras_ignoradas' seja inválido
        raise TypeError("A variável 'palavras_ignoradas' deve ser uma lista!")

    contador_palavras = Counter(texto.split())
    for preposicao in palavras_ignoradas:
        contador_palavras.__delitem__(preposicao)
    return contador_palavras.most_common(quantidade)


def gerar_tag_cloud_por(df, coluna, caminho, dividir_por):
    """Encontra as plavras mais comuns e cria uma 'tag cloud' para cada valor em 'dividir_por', com os dados de uma das colunas do dataframe

    :param df: Dataframe que será utilizado para a criação dos dados
    :type df: pandas.DataFrame
    :param coluna: Título da coluna cujos dados serão obtidos
    :type coluna: str
    :param caminho: Caminho da pasta onde os arquivos png das tag clouds serão geradas
    :type caminho: str
    :param dividir_por: Título da coluna cujos dados serão utilizados para separar as análises
    :type dividir_por: str
    :return: Dicionário com os nomes dos álbums e as palavras mais presentes
    :rtype: dict
    """

    if not isinstance(df, pd.DataFrame):
        # Levanta um erro caso o tipo de 'df' seja inválido
        raise TypeError("A variável 'df' deve ser um Dataframe!")
    if not isinstance(caminho, str):
        # Levanta um erro caso o tipo de 'caminho' seja inválido
        raise TypeError("A variável 'caminho' deve ser do tipo 'str'!")
    
    if coluna not in df.columns:
        # Checa se existe a coluna fornecida no Dataframe
        raise ValueError(f"Não existe a coluna {coluna} no DataFrame fornecido!")
    if dividir_por not in df.columns:
        # Checa se existe a coluna fornecida no Dataframe
        raise ValueError(f"Não existe a coluna {dividir_por} no DataFrame fornecido!")
    
    bases_unicas = set(df[dividir_por]) # Encontra as bases únicos 
    mais_comuns = {}
    for base in bases_unicas: # Loop que percorre por cada base
        df_base = df.loc[df[dividir_por] == base] # Seleciona a parte do dataframe de cada base
        mais_comuns[base] = palavras_comuns(df_base, coluna, f"{caminho}/{coluna} - {base}.png") # Chama a função para gerar as Tag Clouds
    return mais_comuns


def proporção_comparativa(df, coluna, dividir_por):
    """Fornece a proprção de palavras de uma coluna 'coluna' em cada coluna 'dividir_por'

    :param df: Dataframe que será utilizado para a criação dos dados
    :type df: pandas.DataFrame
    :param coluna: Título da coluna cujos dados serão obtidos
    :type coluna: str
    :param dividir_por: Título da coluna cujos dados serão utilizados para separar as análises
    :type dividir_por: str
    :return: Dicionário com cada valor em 'dividido_por' e sua proporção
    :rtype: dict
    """

    if not isinstance(df, pd.DataFrame):
        # Levanta um erro caso o tipo de 'df' seja inválido
        raise TypeError("A variável 'df' deve ser um Dataframe!")
    
    if coluna not in df.columns:
        # Checa se existe a coluna fornecida no Dataframe
        raise ValueError(f"Não existe a coluna {coluna} no DataFrame fornecido!")
    if dividir_por not in df.columns:
        # Checa se existe a coluna fornecida no Dataframe
        raise ValueError(f"Não existe a coluna {dividir_por} no DataFrame fornecido!")

    bases_unicas = set(df[dividir_por])
    contagem_dict = {}
    for base in bases_unicas:
        df_base = df.loc[df[dividir_por] == base] # Seleciona a parte do dataframe de cada álbum
        
        unicos = set(df_base[coluna].tolist()) # Encontra os valores únicos nessa coluna
        unicos_str = {str(elemento) for elemento in unicos} # Transforma cada elemento em string
        palavras = " ".join(unicos_str) # Junta todos esses elementos em uma só string
        palavras_alfanum = re.sub('[^A-Za-z0-9\']+', ' ', palavras).lower() # Remove os caracteres especiais do nome do álbum
        contador = Counter(palavras_alfanum.split())
        total = 0
        for palavra in contador:
            if palavra != " " and palavra != "nan":
                total += contador[palavra]
        base_alfanum = re.sub('[^A-Za-z0-9\']+', ' ', str(base).lower()) # Remove os caracteres especiais do nome do álbum
        i = 0
        for palavra in base_alfanum.split():
            i += contador[palavra]
        contagem_dict[base] = (f"{i}/{total}")
    return contagem_dict
