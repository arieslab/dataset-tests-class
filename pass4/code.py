# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 18:43:00 2020

@author: JJSS
"""

import pandas as pd

#carrega o dataframe para a memoria
df = pd.read_csv('data_result.csv')

#deixa apenas os projetos que são Java
df = df.loc[lambda x: x.language == "Java"]

#função normalizadora, coloca os valores da coluna passada entre 0 e 1 em uma nova coluna
def normalize(df, colName, colNameN):
    result = df.copy()
    max_value = df[colName].max()
    min_value = df[colName].min()
    result[colNameN] = (df[colName] - min_value) / (max_value - min_value)
    return result

#normaliza os valores
df = normalize(df, 'forks_count', 'forks_count_normalized')
df = normalize(df, 'stargazers', 'stargazers_normalized')

#cria uma coluna de classificação, somando os valores normalizados
df['classification'] = df['forks_count_normalized'] + df['stargazers_normalized']

#deleta as colunas que foram criadas para gerar a classificação
df = df.drop(columns=['forks_count_normalized','stargazers_normalized'])

#ordena as linhas pela sua classificação
df = df.sort_values(by=['classification'], ascending=False)

#895 equivalem a 5% do dataframe
df = df.iloc[:804,:]

print(sum(df['tests_count']))

#salva o resultado no results.csv
df.to_csv('results.csv', encoding='utf-8', index=False)
