# -*- coding: utf-8 -*-
"""001_LINKEDIN_SOCIAL_MEDIA_TRATAMENTO_DE_DADOS_Nivel_Pandas

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WXjY6Jf9ayKAqc29Val1zkP82wwYef4O

#**Importações**

***Bibliotecas e instalações***
"""

pip install pandera

import pandas as pd
import pandera as pa
from google.cloud import storage
from matplotlib import pyplot as plt
import os

pip install fsspec

pip install gcsfs

"""***Importando DataFrame***"""

df = pd.read_csv(r'gs://projetofinalgrupo8/entrada/LinkedIn_Profile_Data.csv')

df.head(10)

"""#**Exploração dos dados**

***Verificando valores da coluna***
"""

df.avg_time_in_previous_position.unique()

"""***Listando e verificando colunas especificas***"""

df[['avg_time_in_previous_position','ethnicity','gender',	'glass','m_urn_id','no_of_previous_positions']].head(20)

"""***Verificando dimensão do DataFrame***"""

df.shape

"""***Visualizando colunas existentes***"""

df.columns

"""#Backup"""

df2 = df.copy()

df2.head(13)

"""#Dropando colunas

"""

df2.shape

"""***Removendo colunas irrelevantes***"""

df2 = df2.drop(['c_id','m_urn','avg_current_position_length','no_of_promotions','head_pitch','head_roll','head_yaw', 
                'mouth_close', 'mouth_mask', 'mouth_open','mouth_other','beauty',
                'skin_acne', 'skin_dark_circle', 'skin_health','skin_stain',
                'african', 'celtic_english','east_asian', 'european', 'greek',
                'hispanic', 'jewish', 'muslim','nordic', 'south_asian','beauty_female', 
                'beauty_male','avg_previous_position_length'], axis=1)

"""***Visualizando colunas restantes***"""

df2.columns

"""***Removendo linhas com 'm_urn_id' repetidos***"""

df2 = df2.drop_duplicates(subset=['m_urn_id'])

df2.head(10)

"""#Renomeando colunas

***Criando listas para renomear colunas***
"""

col_old = ['avg_time_in_previous_position', 'm_urn_id', 
           'no_of_previous_positions', 'age','blur', 'emo_anger', 
           'emp_disgust', 'emo_fear', 'emo_happiness','emo_neutral', 'emo_sadness','emo_surprise', 'ethnicity', 
           'gender', 'glass', 'smile', 'nationality','n_followers', 'face_quality']

col_new = ['tempo_cargo_anterior', 'id_usuario', 'promocoes','dias_cargo_anterior',
           'idade', 'desfoque', 'raiva', 'desgosto', 'medo','felicidade','neutro','triste', 'surpresa', 
           'etnia', 'genero', 'oculos','sorriso','nacionalidade','seguidores', 'qualidade_imagem']

df2.columns = col_new

"""***Verificando colunas renomeadas***"""

df2.columns

"""#Identificando as colunas a serem traduzidas

***Selecionando apenas as colunas com string***
"""

df2.select_dtypes(include='object')

"""#Vericando e modificando a coluna 'etnia'

***Consultando valores da coluna***
"""

df2['etnia'].unique()

df2.groupby(["etnia"]).genero.count().plot.bar(figsize=(12,7))

"""***Realizando alterações dos valores***"""

etnias_antigas = ['Asian', 'Black', 'White']
etnias_novas = ['Asiático','Negro','Branco']

df2['etnia'] = df2['etnia'].replace(etnias_antigas, etnias_novas)

"""#Vericando e modificando a coluna 'genero'

***Verificando valores da coluna***
"""

df2['genero'].unique()

df2.groupby(["genero"]).genero.count().plot.pie(figsize=(12,7))

"""***Realizando alterações dos valores***"""

generos_antigos = ['Male','Female']
generos_novos = ['Masculino','Feminino']

df2['genero'] = df2['genero'].replace(generos_antigos, generos_novos)

"""#Vericando e modificando a coluna 'oculos'

***Verificando valores da coluna***
"""

df2.groupby(["oculos"]).genero.count().plot.bar(figsize=(12,7))

df2['oculos'].unique()

"""***Realizando alterações dos valores***"""

oculos_antigos = ['Normal', 'None', 'Dark']
oculos_novos = ['Oculos_comum', 'Nenhum', 'Oculos_escuros']

df2['oculos'] = df2['oculos'].replace(oculos_antigos, oculos_novos)

"""#Vericando e modificando a coluna 'nacionalidade'

***Verificando valores da coluna***
"""

df2.groupby(["nacionalidade"]).nacionalidade.count().plot.pie(figsize=(12,7))

df2['nacionalidade'].unique()

"""***Realizando alterações dos valores***"""

nacionalidades_antigas = ['east_asian', 'hispanic', 'celtic_english', 'european', 'muslim',
       'south_asian', 'nordic', 'african', 'jewish', 'greek']
nacionalidades_novas = ['asiatico_leste', 'hispanico', 'ingles', 'europeu', 'muculmano',
       'asiatico_sul', 'nordico', 'africano', 'judeu', 'grego']

df2['nacionalidade'] = df2['nacionalidade'].replace(nacionalidades_antigas, nacionalidades_novas)

"""#Verificando a coluna 'idade'

***Consultando as idades***
"""

df2.groupby(["idade"]).idade.count().plot.line(figsize=(12,7))

df2.idade.unique()

"""***Filtrando idades menores que 16***"""

indexIdades = df2[ df2['idade'] < 16 ].index

"""***Removendo as idades filtradas***"""

df2.drop(indexIdades , inplace=True)

df2.idade.unique()

"""#Verificando inconsistências na coluna 'Cargo'

***Criando uma lista com os 'tempo_cargo_atual' menor que 0***
"""

indexCargos = df2[ df2['dias_cargo_anterior'] < 0 ].index

"""***Removendo valores negativos da coluna***"""

df2.drop(indexCargos , inplace=True)

"""#Verificando os tipos de dados do DataFrame"""

df2.dtypes

"""#Removendo inconsistências nas colunas 'Float'"""

raiva100 = df2[df2["raiva"]> 100].index

df2.drop(raiva100, inplace=True)

medo100 = df2[df2["medo"]> 100].index

df2.drop(medo100, inplace=True)

desgosto100 = df2[df2["desgosto"]> 100].index

df2.drop(desgosto100, inplace=True)

df2.head(5)

"""#Resetando Index

"""

df2 = df2.reset_index(drop=True)

df2.tail()

"""#Validando Schema"""

schema = pa.DataFrameSchema(
    columns = {
        "tempo_cargo_anterior":pa.Column(pa.Float),
        "id_usuario":pa.Column(pa.Int),
        "promocoes":pa.Column(pa.Int),
        "dias_cargo_anterior":pa.Column(pa.Int),
        "idade":pa.Column(pa.Int),
        "desfoque":pa.Column(pa.Float),
        "raiva":pa.Column(pa.Float),
        "desgosto":pa.Column(pa.Float),
        "medo":pa.Column(pa.Float),
        "felicidade":pa.Column(pa.Float),
        "neutro":pa.Column(pa.Float),
        "triste":pa.Column(pa.Float),
        "surpresa":pa.Column(pa.Float),
        "etnia":pa.Column(pa.String),
        "genero":pa.Column(pa.String),
        "oculos":pa.Column(pa.String),
        "sorriso":pa.Column(pa.Float),
        "nacionalidade":pa.Column(pa.String),
        "seguidores":pa.Column(pa.Int),
        "qualidade_imagem":pa.Column(pa.Float),
    }
)

schema.validate(df2)

"""#Exportando DataFrame para o GCP"""

from google.cloud import storage
import os
serviceAccount = '/content/projetofinalgrupo8-2dcd866c3f46.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = serviceAccount


client = storage.Client()
bucket = client.get_bucket('projetofinalgrupo8')
    
bucket.blob('saida/linkedin_tratado_pandas.csv').upload_from_string(df2.to_csv(index=False), 'text/csv')