import pandas as pd
import plotly.express as px

#formatação para float, antes notação cientifica
pd.options.display.float_format = '{:2f}'.format

#Leitura dos abas do excel "Principal"
df_principal = pd.read_excel("./Imersão Python - Tabela de ações.xlsx",sheet_name="Principal")

#Leitura dos abas do excel "Total_de_acoes"
df_Total_acoes = pd.read_excel("./Imersão Python - Tabela de ações.xlsx",sheet_name="Total_de_acoes")
#df_Total_acoes.head(10)

#Leitura dos abas do excel "Ticker"
df_Ticker = pd.read_excel("./Imersão Python - Tabela de ações.xlsx",sheet_name="Ticker")
#df_Ticker.head(10)

#Leitura dos abas do excel "Chatgpt"
df_Chatgpt = pd.read_excel("./Imersão Python - Tabela de ações.xlsx",sheet_name="Chatgpt")
#df_Chatgpt.head(10)

#Copia refeita para reescrever o dataframe apenas com essas colunas
df_principal = df_principal[['Ativo',	'Data',	'Último (R$)',	'Var. Dia (%)']].copy()

df_principal = df_principal.rename(columns={'Último (R$)':'valor_final','Var. Dia (%)':'var_dia_pct'}).copy()

#Calculo da variação em porcentagem
df_principal['Var_pct'] = df_principal['var_dia_pct'] / 100

#Calculo do valor inicial
df_principal['valor_inicial'] = df_principal['valor_final'] /( df_principal['Var_pct'] + 1)

#União de tabelas, PROCV usado no excel, basicamente o join do SQL 
df_principal = df_principal.merge(df_Total_acoes, left_on='Ativo', right_on='Código', how='left')

#Tirando a coluna código da tabela
df_principal = df_principal.drop(columns=['Código'])

#Calculo da Variação em reais
df_principal['Variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_inicial'])*df_principal['Qtde. Teórica']

#conversão para int, numero inteiros interpretados como float
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)

#Renomeando coluna
df_principal = df_principal.rename(columns={'Qtde. Teórica':'qtd_teorica'}).copy()

#Aplicando função anonima para cada linha do DF e sob a condição determinando resultado
df_principal['Resultado'] = df_principal['Variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))

#União de tabelas, PROCV usado no excel, basicamente o join do SQL  e remoção da coluna ticker que se repete
df_principal = df_principal.merge(df_Ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])

df_principal = df_principal.merge(df_Chatgpt, left_on='Nome', right_on='Nome da Empresa', how='left')
df_principal = df_principal.drop(columns=['Nome da Empresa'])

df_principal['Cat_idade'] = df_principal['Idade (anos)'].apply(lambda x: 'Mais de 100' if x >= 100 else ('Menos de 50' if x < 50 else 'Entre 50 e 100 anos'))

print(df_principal)

# Calculando o maior valor
maior = df_principal['Variacao_rs'].max()

# Calculando o menor valor
menor = df_principal['Variacao_rs'].min()

# Calculando o media valor
media = df_principal['Variacao_rs'].mean()

# Calculando a média de quem subiu
media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_rs'].mean()

# Calculando a média de quem desceu
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_rs'].mean()

# Imprimindo os resultados
print(f"Maior\tR$ {maior:,.2f}")
print(f"Maior\tR$ {menor:,.2f}")
print(f"Maior\tR$ {media:,.2f}")
print(f"Média de quem subiu\tR$ {media_subiu:,.2f}")
print(f"Média de quem desceu\tR$ {media_desceu:,.2f}")

df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu']

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_rs'].sum().reset_index()
print(df_analise_segmento)

df_analise_saldo = df_principal.groupby('Resultado')['Variacao_rs'].sum().reset_index()
print(df_analise_saldo)

# Exibindo o número de empresas que subiram
contagem_subiu = (df_principal['Resultado'] == 'Subiu').sum()
print("Número de empresas que subiram:", contagem_subiu)

# Exibindo a contagem de empresas em cada faixa de idade
contagem_idade = df_principal.groupby('Cat_idade').size()
print("Contagem de empresas por faixa de idade:")
print(contagem_idade)

fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Resultado')
fig.show()

