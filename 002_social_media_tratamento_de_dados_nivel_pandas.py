# -*- coding: utf-8 -*-
"""002_SOCIAL_MEDIA_TRATAMENTO_DE DADOS_Nivel_Pandas

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C8isdhWYarRfel_dIwKj-aMtJZgAGK4S

#Importações

**Bibliotecas**
"""

pip install pandera

pip install fsspec

pip install gcsfs

from matplotlib import pyplot as plt
from google.cloud import storage
import pandera as pa
import pandas as pd
import numpy as np
import os

"""**Importando DataFrame**"""

df = pd.read_csv(r'gs://projetofinalgrupo8/saida/youtube_data_base.csv')

df.head(2)

"""#Exploração dos dados

**Verificando dimensão do DataFrame**
"""

df.shape

"""**Tipos dos dados**"""

df.dtypes

"""#Backup"""

df2 = df.copy()

"""#Renomeando colunas e dados Categoricos

**Criando listas para renomear colunas**
"""

col_old = ['video_id', 'title', 'publishedAt', 'channelId', 'channelTitle',
       'trending_date', 'view_count', 'likes', 'dislikes', 'comment_count',
       'comments_disabled', 'ratings_disabled', 'country', 'json_title']

col_new = ['id_video', 'titulo_video', 'publicado_em', 'id_canal', 'nome_canal',
           'data_destaque', 'cont_visualizacao', 'curtidas', 'nao_curtidas', 'cont_comentarios',
           'comentarios_desabilitados', 'curtidas_desabilitadas', 'pais', 'categoria']

df2.columns = col_new

df2.head(2)

"""**Vericando tipos de categorias**"""

df2.groupby(["categoria"]).categoria.count().plot.pie(figsize=(12,7))

df2['categoria'].unique()

"""**Criando listas para renomear as categorias**"""

categoria_antiga = ['People & Blogs', 'Music', 'Gaming', 'Comedy', 'Sports',
       'Entertainment', 'Education', 'Autos & Vehicles', 'Howto & Style',
       'News & Politics', 'Science & Technology', 'Film & Animation',
       'Travel & Events', 'Pets & Animals']

categoria_nova = ['pessoas_e_blogs', 'musica', 'jogos', 'comedia', 'esportes',
                  'entretenimento', 'educacao', 'automoveis', 'como_faz_e_estilos',
                  'noticias_e_politicas', 'ciencias_e_tecnologia', 'filme_e_animacao',
                  'viagens_e_eventos', 'animais']

"""**Renomeando categorias**"""

df2['categoria'] = df2['categoria'].replace(categoria_antiga, categoria_nova)

df2.groupby(["pais"]).pais.count().plot.pie(figsize=(12,7))

"""#Formatando datetime

**Verificando os tipos de dados do DataFrame**
"""

df2.dtypes

df2['publicado_em'] = pd.to_datetime(df2['publicado_em']).dt.strftime("%Y-%m-%d %H:%M:%S")
df2['publicado_em'] = pd.to_datetime(df2['publicado_em'])

df2['data_destaque'] = pd.to_datetime(df2['data_destaque']).dt.strftime("%Y-%m-%d")
df2['data_destaque'] = pd.to_datetime(df2['data_destaque'])

df2.dtypes

df2.sample()

df2.groupby(["data_destaque"]).data_destaque.count().plot.line(figsize=(12,7))

"""#Tratando dados nulos

**Verificando números de dados nulos**
"""

df2.isna().sum()

"""**Tratando os valores nulos da coluna "Categoria"**"""

categoria_antiga = ['People & Blogs', 'Music', 'Gaming', 'Comedy', 'Sports',
       'Entertainment', 'Education', 'Autos & Vehicles', 'Howto & Style',
       'News & Politics', 'Science & Technology', 'Film & Animation',
       'Travel & Events', 'Pets & Animals', np.nan]

categoria_nova = ['pessoas_e_blogs', 'musica', 'jogos', 'comedia', 'esportes',
                  'entretenimento', 'educacao', 'automoveis', 'como_faz_e_estilos',
                  'noticias_e_politicas', 'ciencias_e_tecnologia', 'filme_e_animacao',
                  'viagens_e_eventos', 'animais', 'outros']

df2['categoria'] = df2['categoria'].replace(categoria_antiga, categoria_nova)

df2.isna().sum()

"""**Verificando nomes de canais com valor nulo**"""

df2[df2['nome_canal'].isnull()]

"""**Removendo linha com nome de canal nulo**"""

df2.drop(499155, inplace = True)

df2.isna().sum()

"""#Validação dos dados"""

df2.dtypes

schema = pa.DataFrameSchema(
    columns = {
        "id_video":pa.Column(pa.String),
        "titulo_video":pa.Column(pa.String),
        "publicado_em":pa.Column(pa.DateTime),
        "id_canal":pa.Column(pa.String),
        "nome_canal":pa.Column(pa.String),
        "data_destaque":pa.Column(pa.DateTime),
        "cont_visualizacao":pa.Column(pa.Int),
        "curtidas":pa.Column(pa.Int),
        "nao_curtidas":pa.Column(pa.Int),
        "cont_comentarios":pa.Column(pa.Int),
        "comentarios_desabilitados":pa.Column(pa.Bool),
        "curtidas_desabilitadas":pa.Column(pa.Bool),
        "pais":pa.Column(pa.String),
        "categoria":pa.Column(pa.String)
    }
)

schema.validate(df2)

"""#Informações gerais sobre os tipo de dados e quantidades de não nulos"""

df2.info()

"""#Exportando DataFrame para o GCP"""

from google.cloud import storage
import os
serviceAccount = '/content/projetofinalgrupo8-2dcd866c3f46.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = serviceAccount


client = storage.Client()
bucket = client.get_bucket('projetofinalgrupo8')
    
bucket.blob('saida/youtube_tratado_pandas.csv').upload_from_string(df2.to_csv(index=False), 'text/csv')