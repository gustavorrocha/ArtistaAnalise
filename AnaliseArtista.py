import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy

#GRUPO DE PERGUNTAS 1
# Cálculo do máximo e mínimo de aspectos por álbum
def max_e_min_album(df, coluna): 
    """Funçao que calcula o máximo e mínimo de aspectos por álbum

    :param df: Data Frame a ser utilizado
    :type df: pandas.DataFrame
    :param coluna: Aspecto a ser analizado, podendo ser "popularidade" e "duracao"
    :type coluna: str
    :return: As músicas com maiores e menores popularidade ou duração por álbum
    :rtype: pandas.DataFrame
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(coluna, str):
        raise TypeError("A coluna deve ser uma str")
    lista_albuns = []
    try:
        for album in set(df.index.get_level_values("album")): 
            info_album = df.loc[[album]]
            max_album = (info_album[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
            min_album = (info_album[["nome", coluna]].sort_values(by=[coluna])[:3])
            lista_albuns.append(pd.concat([min_album, max_album])) 
        return pd.concat(lista_albuns)

# Cálculo do máximo e mínimo da aspectos em toda a discografia do artista
def max_e_min_musicas(df, coluna):
    """Funçao que calcula o máximo e mínimo de aspectos por álbum

    :param df: Data Frame a ser utilizado
    :type df: pandas.DataFrame
    :param coluna: Aspecto a ser analizado, podendo ser "popularidade" e "duracao"
    :type coluna: str
    :return: As músicas com maiores e menores popularidade ou duração na carreira do artista
    :rtype: pandas.DataFrame
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(coluna, str):
        raise TypeError("A coluna deve ser uma str")
    try:
        max_musicas = (df[["nome", coluna]].sort_values(by=[coluna], ascending=False)[:3])
        min_musicas = (df[["nome", coluna]].sort_values(by=[coluna])[:3])
        return pd.concat([max_musicas, min_musicas], ignore_index=True, axis=0)
    except KeyError:
       print(f'A entrada {coluna} não é uma coluna válida do df. Tente uma coluna existente.')
    
# Visualização do máximo e mínimo de aspectos por álbum
def visualizacao_maxmin_album(df, coluna):
    """Funçao que calcula o máximo e mínimo de aspectos por álbum

    :param df: Data Frame a ser utilizado
    :type df: pandas.DataFrame
    :param coluna: Aspecto a ser analizado, podendo ser "popularidade" e "duracao"
    :type coluna: str
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(coluna, str):
        raise TypeError("A coluna deve ser uma str")
    try:
        principal = max_e_min_album(df, coluna)
        fig = sns.barplot(data = principal, x = coluna, y = "nome") # Criando o gráfico de barras
        plt.savefig ("./graficoalbum", dpi=600)
    except KeyError:
       print(f'A entrada {coluna} não é uma coluna válida do df. Tente uma coluna existente.')

# Visualização do máximo e mínimo de aspectos em toda a discografia do artista
def visualizacao_maxmin_musicas(df, coluna):
    """Funçao que calcula o máximo e mínimo de aspectos por álbum

    :param df: Data Frame a ser utilizado
    :type df: pandas.DataFrame
    :param coluna: Aspecto a ser analizado, podendo ser "popularidade" e "duracao"
    :type coluna: str
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(coluna, str):
        raise TypeError("A coluna deve ser uma str")
    try:
        principal = max_e_min_musicas(df, coluna)
        fig = sns.barplot(data = principal, x = "nome", y = coluna) #Criando gráfico em barras
        plt.savefig ("./graficodiscografia", dpi=600)
    except KeyError:
       print(f'A entrada {coluna} não é uma coluna válida do df. Tente uma coluna existente.')
    
# Função que retorna resumo dos albuns mais premiados com a respectiva quantidade de premios de album e musica
def albuns_mais_premiados(df, top):
    """Função retorna um resumo dos albuns e quantidade de premios dos albuns e das musicas do album
    
    :param df: DataFrame com todas as informações dos premios de musica, album etc de um artista 
    :type df: pandas.DataFrame
    :param top: numero max do topo do rank de albusn mais premiados
    :type variavel: int
    :return: Retorna uma dataframe com resumo dos premios por albuns
    :rtype: pd.DataFrame
    """
    if not isinstance(top, int):
        raise TypeError('A entrada top deve ser um número inteiro.')
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    dfcopy = df.copy()
    try:
        dfcopy = dfcopy[dfcopy["premios do album"].notnull()][["premios do album"]].drop_duplicates()
    except KeyError:
        print("A coluna 'premios do album' não existe!")
        return
    dfcopy["quantidade de premios"] = dfcopy["premios do album"].str.split(" & ").apply(len)
    return dfcopy[:top][["quantidade de premios"]]

# Função que avalia a relação entre a duração da música e algumas variaveis da discografia
def corr_com_tempo(df, variavel):
    """Função dá correlçao entre uma variavel da dsicografia e a duração da musica
    
    :param df: DataFrame com todas as informações dos premios de musica, album etc de um artista 
    :type df: pandas.DataFrame
    :param variavel: Nivel de agregação da analise de correlação 
    :type variavel: str
    :return: valor da correlaçao 
    :rtype: float
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(variavel, str):
        raise TypeError("A variavel deve ser do tipo str")
    variaveis_aceitas = ['popularidade','volume', 'bpm', 'energia', 'fala', 'acustica', 'instrumentalidade', 'valencia' ]
    if variavel not in variaveis_aceitas:
        raise ValueError('A entrada da variavel não é um valor aceito!')
    dfcopy = df.copy()
    try:
        minutos = dfcopy["duracao"].str.split(":", expand=True)[0].apply(int)*60
        segundos = dfcopy["duracao"].str.split(":", expand=True)[1].apply(int)
        duracao = np.array(minutos + segundos)
    except KeyError:
        print("A coluna duração nao existe!")
        return
    var = np.array(dfcopy[variavel].apply(float))
    print(f"A correlção entre a duração da musica e {variavel} é: ")
    return np.corrcoef(duracao, var)[0][1]  
 

#GRUPO DE PERGUNTAS 3
#PERGUNTAS SUGERIDAS



#  Frenquencia do modo (maior ou menor) de toda a discografia, por album ou por musica.
def porcentagem_modo(df, variavel):
    """Função dá a porcentagem que cada modo aparece em nivel de album ou do conjunto total de musicas
    
    :param df: DataFrame com todas as informações dos premios de musica, album etc de um artista 
    :type df: pandas.DataFrame
    :param variavel: Nivel de agregação da analise de porcentagem. Pode assumir valor 'album' ou 'musica'
    :type variavel: str
    :return: um df com a resposta
    :rtype: pandas.DataFrame
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(variavel, str):
        raise TypeError("A variavel deve ser uma str")
    if variavel != 'album' and variavel != 'musica':
        raise TypeError('A entrada de variavel não é valida. Deve ser "musica" ou "album"')
    try:
        if variavel == 'album':
            df_perc = df.groupby([df.index]).agg({'modo': 'size'}) 
            df_modo0 = pd.DataFrame(df[df["modo"] == 0].groupby([df[df["modo"] == 0].index]).agg({'modo': 'size'}))
            df_modo1 = pd.DataFrame(df[df["modo"] == 1].groupby([df[df["modo"] == 1].index]).agg({'modo': 'size'}))
            df_perc = df_perc.merge(df_modo0, left_index=True, right_index=True)
            df_perc = df_perc.merge(df_modo1, left_index=True, right_index=True)
            df_perc.columns = ['total', 'modo 0', 'modo 1']
            df_perc['% modo 0'], df_perc['% modo 1']= df_perc['modo 0']/df_perc['total'], df_perc['modo 1']/df_perc['total']
            return df_perc[['% modo 0', '% modo 1']]
        if variavel == 'musica':
            df_perc_musica = df[["nome", "modo"]].drop_duplicates(["nome", "modo"])
            return df_perc_musica.groupby("modo").agg({'modo': 'size'}) / len(df_perc_musica["nome"])
    except Exception as error:
        print('Erro:', error)
    
 


# Comparar popularidade media do album com quantidade de premiações do album e suas musica
def comparar_popularidade_premios(df):
    """Função dá a porcentagem que cada modo aparece em nivel de album ou do conjunto total de musicas
    
    :param df: DataFrame com todas as informações dos premios de musica, album e do artista 
    :type df: pandas.DataFrame
    :return: um df com a resposta
    :rtype: pandas.DataFrame
    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    try: 
        df_temp = df[['premios da musica']].dropna()
        temp = df_temp.groupby([df_temp.index])['premios da musica'].transform(lambda x: ' & '.join(x)).drop_duplicates()
        df_musica = pd.DataFrame(temp)
        df_musica['quant de premios da musica'] = df_musica["premios da musica"].str.split(" & ").apply(len)
        df_album = df[['premios do album']].dropna()
        df_album = df_album.drop_duplicates()
        df_album['quant de premios do album'] = df_album["premios do album"].str.split(" & ").apply(len)
        df_quant = pd.merge(df_musica, df_album, left_index=True, right_index=True)[['quant de premios da musica', 'quant de premios do album']]
        df_pop = df.groupby(df.index)['popularidade'].mean()
        pd_resposta = pd.merge(pd.DataFrame(df_pop), df_quant , how='left', left_index=True, right_index=True)
        return pd_resposta
    except Exception as error:
        print('Erro:', error)

        
        
# Comparar duas colunas do data frame por meio de visualização grafica e de regressão linear
def plot(data, coluna1, coluna2 ):
    """Função que plota um graficom e a regressão linear de duas colunas do df
    
    :param data: DataFrame com todas as informações dos premios de musica, album etc de um artista 
    :type data: pandas.DataFrame
    :param coluna1: nome de uma coluna do DataFrame 
    :type coluna1: str
    :param coluna2: nome de uma coluna do DataFrame para ser comparada com a anterior - coluna1
    :type coluna1: str
    :return: Visualização da regressão linear das duas variáveis
    :rtype: matplotlib Axes
    """
    variaveis_aceitas = ['popularidade','volume', 'bpm', 'energia', 'fala', 'acustica', 'instrumentalidade', 'valencia' ]
    if not isinstance(data, pd.core.frame.DataFrame):
        raise TypeError("O df deve ser um pd.DataFrame")
    if not isinstance(coluna1, str):
        raise TypeError("A entrada da coluna1 deve ser uma str")
    if not isinstance(coluna2, str):
        raise TypeError("A entrada da coluna2 deve ser uma str")
    if coluna1 not in variaveis_aceitas:
        raise ValueError('A entrada para a coluna1 não é um valor aceito!')
    if coluna2 not in variaveis_aceitas:
        raise ValueError('A entrada para a coluna2 não é um valor aceito!')
    try:
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(data[coluna1],data[coluna2])
        fig = ax = sns.regplot(x=data[coluna1], y=data[coluna2], data=data , color='b', line_kws={'label':"y={0:.4f}x+{1:.2f}".format(slope,intercept)})
        ax.legend()
        return fig.plot()
    except Exception as error:
        print("Não foi possivel gerar a visualização: ", error)

    
ARTISTA = "Adele"
dados_df = pd.read_csv(f"./Infos/{ARTISTA}.csv", sep=";", encoding="utf-8-sig")

# Chama a função com os apectos de popularidade e duração por álbum
max_e_min_album(dados_df, "popularidade")
max_e_min_album(dados_df, "duracao")

# Chama a função com os apectos de popularidade e duração em toda a discografia do artista
max_e_min_musicas(dados_df, "popularidade")
max_e_min_musicas(dados_df, "duracao")

# Chama a visualização com os apectos de popularidade e duração em toda a discografia do artista
visualizacao_maxmin_musicas(dados_df, "popularidade")
visualizacao_maxmin_musicas(dados_df, "duracao")

# Chama a função com os albuns mais premiados 
albuns_mais_premiados(dados_df, 3)  

# Chama a função com a correlação entre duração da música e alguma variável
corr_com_tempo(dados_df,"popularidade")

