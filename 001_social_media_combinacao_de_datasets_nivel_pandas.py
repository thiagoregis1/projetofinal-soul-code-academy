# -*- coding: utf-8 -*-
"""001_SOCIAL_MEDIA_COMBINACAO_DE_DATASETS_Nivel_Pandas

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WnvhPZPWyKgbGIbuDqBOdxzxD0CZp-x0

#Importações

**BIBLIOTECAS**
"""

pip install fsspec

pip install gcsfs

import pandas as pd

"""**CARREGANDO DATAFRAME PAISES** 
DATASETS EXTRAÍDOS DO KAGGLE NO DIA 17/11/2021
"""

dados_br_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/BR_youtube_trending_data.csv')
dados_ca_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/CA_youtube_trending_data.csv')
dados_de_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/DE_youtube_trending_data.csv')
dados_fr_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/FR_youtube_trending_data.csv')
dados_gb_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/GB_youtube_trending_data.csv')
dados_in_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/IN_youtube_trending_data.csv')
dados_jp_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/JP_youtube_trending_data.csv')
dados_kr_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/KR_youtube_trending_data.csv')
dados_mx_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/MX_youtube_trending_data.csv')
dados_us_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/US_youtube_trending_data.csv')
dados_ru_csv = pd.read_csv('gs://projetofinalgrupo8/entrada/RU_youtube_trending_data.csv')

dados_br_csv.shape

"""#Criação de colunas, exploração e união dos Datasets

**ADICIONANDO COLUNA COM ABREVIAÇÃO DO PAÍS**
"""

dados_br_csv['country'] = 'BR'
dados_ca_csv['country'] = 'CA'
dados_de_csv['country'] = 'DE'
dados_fr_csv['country'] = 'FR'
dados_gb_csv['country'] = 'GB'
dados_in_csv['country'] = 'IN'
dados_jp_csv['country'] = 'JP'
dados_kr_csv['country'] = 'KR'
dados_mx_csv['country'] = 'MX'
dados_us_csv['country'] = 'US'
dados_ru_csv['country'] = 'RU'

"""**VERIFICANDO DIMENSÃO DE CADA PAÍS**"""

print(f' BR: {dados_br_csv.shape},\n CA: {dados_ca_csv.shape},\n DE: {dados_de_csv.shape},\n FR: {dados_fr_csv.shape},\n GB: {dados_gb_csv.shape},\n IN: {dados_in_csv.shape},\n JP: {dados_jp_csv.shape},\n KR: {dados_kr_csv.shape},\n MX: {dados_mx_csv.shape},\n US: {dados_us_csv.shape},\n RU: {dados_ru_csv.shape}')

"""**CONCATENANDO DADOS WORLD**"""

dataframes = [dados_br_csv, dados_ca_csv, dados_de_csv, dados_fr_csv, dados_gb_csv, dados_in_csv, dados_jp_csv, 
              dados_kr_csv, dados_mx_csv, dados_us_csv, dados_ru_csv]
dados_world_csv = pd.concat(dataframes)

"""**VERIFICANDO DADOS WORLD**"""

dados_world_csv.shape

"""**CARREGANDO JSON COMPLEMENTAR DE PARA DADOS WORLD**"""

dados_json = pd.read_json('gs://projetofinalgrupo8/entrada/BR_category_id.json')

"""**EXPLORANDO JSON**"""

dados_json.sample()

dados_json['items'][0]

"""**DESCOMPRIMINDO JSON**"""

new_dados = []

for i in range(len(dados_json['items'])):
  #print(dados_json['items'][i])
  new_data = {}
  new_data['json_kind'] = dados_json['items'][i]['kind']
  new_data['json_etag'] = dados_json['items'][i]['etag']
  new_data['categoryId'] = dados_json['items'][i]['id']
  new_data['json_title'] = dados_json['items'][i]['snippet']['title']
  new_data['json_assignable'] = dados_json['items'][i]['snippet']['assignable']
  new_data['json_channelId'] = dados_json['items'][i]['snippet']['channelId']
  new_dados.append(new_data)

new_df = pd.DataFrame(new_dados)

new_df.dtypes

new_df['categoryId'] = new_df['categoryId'].astype('int64')

new_df.dtypes

"""**COMBINANDO DADOS WORLD COM JSON**"""

data_raw = pd.merge(dados_world_csv, new_df, on=['categoryId'], how='left')

data_raw.shape

data_raw.head(3)

data_raw.dtypes

"""#Removendo colunas
Optamos por remover essas colunas por serem relevantes para o nosso projeto
"""

data_raw2 = data_raw.drop(['categoryId', 'tags', 'thumbnail_link', 'description', 'json_kind', 'json_etag', 'json_assignable', 'json_channelId'], axis=1)

data_raw2.shape

"""#Exportando para o GCP"""

from google.cloud import storage
import os
serviceAccount = '/content/projetofinalgrupo8-2dcd866c3f46.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = serviceAccount


client = storage.Client()
bucket = client.get_bucket('projetofinalgrupo8')
    
bucket.blob('saida/youtube_data_base.csv').upload_from_string(data_raw2.to_csv(index=False), 'text/csv')